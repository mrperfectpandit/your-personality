import string
import re
from transformers import AutoTokenizer,TFBertModel
import tensorflow as tf
from scipy import stats
import pandas as pd
import numpy as np
from tensorflow.keras.models import load_model

maxlen = 1500
per_types = ['ENFJ','ENFP','ENTJ','ENTP','ESFJ','ESFP','ESTJ','ESTP','INFJ','INFP','INTJ','INTP','ISFJ','ISFP','ISTJ','ISTP']


def clean_text(text):
    regex = re.compile('[%s]' % re.escape('|'))
    text = regex.sub(" ", text)
    words = str(text).split()
    words = [i.lower() + " " for i in words]
    words = [i for i in words if not "http" in i]
    words = " ".join(words)
    words = words.translate(words.maketrans('', '', string.punctuation))
    return words


def recreate_model(): 
    input_word_ids = tf.keras.layers.Input(shape=(maxlen,), dtype=tf.int32,
                                           name="input_word_ids")
    bert_layer = TFBertModel.from_pretrained("bert-base-uncased")
    bert_outputs = bert_layer(input_word_ids)[0]
    pred = tf.keras.layers.Dense(16, activation='softmax')(bert_outputs[:,0,:])
    
    model = tf.keras.models.Model(inputs=input_word_ids, outputs=pred)
    loss = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)
    model.compile(loss='categorical_crossentropy', optimizer=tf.keras.optimizers.Adam(
    learning_rate=0.00001), metrics=['accuracy'])
    model.load_weights("model/bert_base_model.h5")
    return model

new_model = recreate_model()
tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
# new_model = load_model('model/bert_base_model.h5')

def predict_type(text):
    cleaned_text = clean_text(text)
    custom_test_ids = [tokenizer.encode(str(cleaned_text))]
    type_index = np.argmax(new_model.predict(np.array(custom_test_ids)))
    return (per_types[type_index])

def predict_tweet(username):
    df_tweet_path = "twitter_data/tweets_"+str(username)+".csv"
    tweet_csv = pd.read_csv(df_tweet_path)
    tweet_csv = tweet_csv[["0"]]
    tweet_csv["cleaned"] = tweet_csv["0"].apply(clean_text)
    tweet_ids = [tokenizer.encode(str(i), max_length = 50 , pad_to_max_length = True) for i in tweet_csv.cleaned.values]
    tweet_values = new_model.predict(np.array(tweet_ids))
    tweet_index = tweet_values.argmax(axis=1)
    per_operation = per_types[stats.mode(tweet_index).mode[0]]
    
    json_operation = {}
    json_operation["name"] = str(username)
    json_operation["type"] = str(per_operation)
    predict_values = np.sum(tweet_values,axis = 0)
    # summer = np.sum(predict_values)
    intro = np.sum(predict_values[8:])/np.sum(predict_values)*100
    intui = np.sum(predict_values[0:4]+predict_values[8:12])/np.sum(predict_values)*100
    feeli = np.sum(predict_values[0:2]+predict_values[4:6] + predict_values[8:10] + predict_values[12:14])/np.sum(predict_values)*100
    judgi = np.sum(predict_values[::2]/np.sum(predict_values)*100)
    info_df = pd.read_csv("data/MBTI_types.csv")
    json_operation["introvertism"] = int(intro)
    json_operation["extrovertism"] = int(100-intro)
    json_operation["intuition"] = int(intui)
    json_operation["sensing"] = int(100-intui)
    json_operation["feeling"] = int(feeli)
    json_operation["thinking"] = int(100-feeli)
    json_operation["judging"] = int(judgi)
    json_operation["perceiving"] = int(100-judgi)
    json_operation["traits"] = info_df[info_df["type"]==per_operation]["traits"].values[0]
    json_operation["career"] = info_df[info_df["type"]==per_operation]["career"].values[0]
    json_operation["people"] = info_df[info_df["type"]==per_operation]["eminent personalities"].values[0]
    json_operation["per_name"] = info_df[info_df["type"]==per_operation]["name"].values[0]
    per_file = open("static/results_personality.js","w")

    

    per_str = "var personality_data="+str(json_operation)+"\n"+";export {personality_data};"
    per_file.write(per_str)
    per_file.close()
    predict_follow(username)
    return json_operation

def predict_follow(username):
    df_follow_path = pd.read_csv("twitter_data/fol_"+str(username)+".csv")
    follow_json = {}
    follow_ids = {}
    for i in range(5):
        list_ = df_follow_path.tweets.iloc[i].split(", \'")
        new_list = []
        for j in list_:
            new_list.append(clean_text(j))
        tweet_ids = [tokenizer.encode(str(k), max_length = 100 , pad_to_max_length = True) for k in new_list]
        tweet_values = new_model.predict(np.array(tweet_ids))
        tweet_index = tweet_values.argmax(axis=1)
        print (per_types[stats.mode(tweet_index).mode[0]])
        follow_json[str(i)] = per_types[stats.mode(tweet_index).mode[0]]
        follow_ids[str(i)] = df_follow_path.follower.iloc[i]
        per_file = open("static/results_follower.js","w")
        per_str = "var follower_data="+str(follow_json)+"\n"
        follow_str = "var follower_ids="+str(follow_ids)+"\n"
        per_file.write(per_str)
        per_file.write(follow_str)
        per_file.close()
    return follow_json
    


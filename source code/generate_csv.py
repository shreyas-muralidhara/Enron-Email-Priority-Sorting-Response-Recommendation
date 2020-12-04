from os import listdir
import re
import csv
import ast
import pandas as pd
import datetime
import dateutil.parser


def read_dir(filename):
    return listdir(filename)

def convert_str_list_to_list(str_list):
    ast.literal_eval(str_list)

def get_deleted_email_list(deleted_email_filename):
    file_list = read_dir(deleted_email_filename)
    return_list = []
    for file in file_list:
        f = open(deleted_email_filename+'/'+file, "r")
        s = f.read()
        # print(s)
        To_list = re.findall('To: \S+',s)
        for i in range(len(To_list)):
            To_list[i] = To_list[i].lstrip('To: ')
        Title_list = re.findall('Subject:[\S\d ]+',s)
        for i in range(len(Title_list)):
            Title_list[i] = Title_list[i].lstrip('Subject: ')
        From_list = re.findall('From: \S+',s)
        From_list[0] = From_list[0].lstrip('From: ')
        temp =  Date_list[0].lstrip('Date: ')
        yourdate = dateutil.parser.parse(temp)
        yourdate = yourdate.strftime("%Y-%m-%d %H:%M:%S")
        Date_list[0] = yourdate
        subject_list = re.findall('X-FileName: [\r \n \S \d  ]+',s)
        for i in range(len(subject_list)):
            subject_list[i] = subject_list[i].lstrip('X-FileName: ')
        if len(To_list)==0:
            continue
        if len(Title_list)==0:
            continue
        if len(Date_list)==0:
            continue
        if len(From_list)==0:
            continue
        with open('data_generated.csv', 'a', newline='') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
            spamwriter.writerow([To_list[0] ,From_list[0], Date_list[0], subject_list, Title_list[0],'delete',deleted_email_filename+'/'+file])

def get_sent_email_list(sent_email_filename):
    file_list = read_dir(sent_email_filename)
    return_list = []

    for file in file_list:
        f = open(sent_email_filename+'/'+file, "r")
        s = f.read()
        To_list = re.findall('To: [\S\d ]+',s)
        for i in range(len(To_list)):
            To_list[i] = To_list[i].lstrip('To: ')
        Title_list = re.findall('Subject:[\S\d ]+',s)
        for i in range(len(Title_list)):
            Title_list[i] = Title_list[i].lstrip('Subject: ')
        From_list = re.findall('From: \S+',s)
        From_list[0] = From_list[0].lstrip('From: ')
        Date_list = re.findall('Date: [\S\d ]+',s)

        temp =  Date_list[0].lstrip('Date: ')
        yourdate = dateutil.parser.parse(temp)
        yourdate = yourdate.strftime("%Y-%m-%d %H:%M:%S")
        Date_list[0] = yourdate
        subject_list = re.findall('X-FileName: [\r \n \S ]+',s)
        for i in range(len(subject_list)):
            subject_list[i] = subject_list[i].lstrip('X-FileName: ')
        # return_list.append([To_list ,From_list[0], Date_list, subject_list, 'reply'])
        if len(To_list)==0:
            continue
        if len(Title_list)==0:
            continue
        if len(Date_list)==0:
            continue
        if len(From_list)==0:
            continue
        with open('data_generated.csv', 'a', newline='') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
            spamwriter.writerow([To_list[0] ,From_list[0], Date_list[0], subject_list,Title_list[0],'reply', sent_email_filename+'/'+file])

def get_thread_email_list(thread_email_filename):
    file_list = read_dir(thread_email_filename)
    return_list = []
    for file in file_list:
        f = open(thread_email_filename+'/'+file, "r")
        s = f.read()
        To_list = re.findall('To: \S+',s)
        for i in range(len(To_list)):
            To_list[i] = To_list[i].lstrip('To: ')

        Title_list = re.findall('Subject:[\S\d ]+',s)
        for i in range(len(Title_list)):
            Title_list[i] = Title_list[i].lstrip('Subject: ')
        From_list = re.findall('From: \S+',s)
        From_list[0] = From_list[0].lstrip('From: ')
        Date_list = re.findall('Date: [\S\d ]+',s)

        if len(Date_list)==0:
            continue
        temp =  Date_list[0].lstrip('Date: ')
        yourdate = dateutil.parser.parse(temp)
        yourdate = yourdate.strftime("%Y-%m-%d %H:%M:%S")
        Date_list[0] = yourdate
        subject_list = re.findall('X-FileName: [\r \n \S \d  ]+',s)
        for i in range(len(subject_list)):
            subject_list[i] = subject_list[i].lstrip('X-FileName: ')
        if len(Date_list)==0:
            continue
        # return_list.append([To_list[0] ,From_list, Date_list[0], subject_list])
        if len(To_list)==0:
            continue
        if len(Title_list)==0:
            continue
        if len(From_list)==0:
            continue

        with open('data_generated.csv', 'a', newline='') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
            spamwriter.writerow([To_list[0] ,From_list[0], Date_list[0], subject_list, Title_list[0], 'thread', thread_email_filename+'/'+file])


def get_email_list(filename, directory_list):
    sent_mail_list,discussion_threads, deleted_mail_list, spam_email_list = [],[],[],[]
    with open('data_generated.csv', 'a', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(['To_list' ,'From_list', 'Date_list', 'subject_list','Title','Label','file'])
    deleted_email_filename = filename+'/deleted_items'
    deleted_mail_list = get_deleted_email_list(deleted_email_filename)
    sent_email_filename = filename+'/sent'
    sent_mail_list = get_sent_email_list(sent_email_filename)
    thread_email_filename = filename+'/discussion_threads'
    sent_mail_list = get_thread_email_list(thread_email_filename)
    return sent_mail_list,discussion_threads, deleted_mail_list, spam_email_list

def clean_data_set():
    df = pd.read_csv('test.csv')
    df['new_list'] = df.To_list.map(lambda line: convert_str_list_to_list(line))
    print(df.new_list)


if __name__ == '__main__':
    filename = './maildir/mann-k'
    directory_list = read_dir(filename)
    sent_mail_list,discussion_threads, deleted_mail_list, spam_email_list = get_email_list(filename, directory_list)

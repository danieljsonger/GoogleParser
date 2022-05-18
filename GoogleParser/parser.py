import json

PAOLA_CHAT_ID = "Ugwx4C9v6z1rQIbGPTh4AaABAagB1uC8Bw" # Chat 7
NABEEL_CHAT_ID = "Ugzl-UkYAtFqhglhoZR4AaABAagBmuasDQ" # Chat 1

DANIEL_USER_ID = "111348785696902170212"
PAOLA_USER_ID = "117020877298064930222"

class ChatParser:
    class Message:
        def __init__(self, timestamp, name, text):
            self.timestamp = timestamp
            self.name = name
            self.text = text

        def to_string(self):
            ret_val = "[" + self.name + "]:\t"
            # if self.name == "Paola":
            #     ret_val = ret_val + "\t\t"
            # else:
            #     ret_val = ret_val + "\t"

            return ret_val + self.text + "\n"

    def __init__(self, filename):
        print("Creating new parsed chat")
        file = open(filename, "r")
        file_str = file.read()
        file.close()
        self.chat_dict = json.loads(file_str)

    def load_chat(self):

        # Primer
        self.texts = []
        name = ""
        timestamp = self.chat_dict['conversations'][7]['events'][0]['timestamp']
        text = ""
        for i in range(len(self.chat_dict['conversations'][7]['events'][0]['chat_message']['message_content']['segment'])):
            text = text + self.chat_dict['conversations'][7]['events'][0]['chat_message']['message_content']['segment'][i]['text']
        if self.chat_dict['conversations'][7]['events'][0]['sender_id']['chat_id'] == PAOLA_USER_ID:
            name = "Paola"
        else:
            name = "Daniel"
        msg = self.Message(timestamp, name, text)
        self.texts.append(msg)

        # Parse all messages
        # print(len(self.chat_dict['conversations'][7]['events']))
        length = len(self.chat_dict['conversations'][7]['events'])
        for i in range(1, length):
            if self.chat_dict['conversations'][7]['events'][i]['sender_id']['chat_id'] == PAOLA_USER_ID:
                name = "Paola"
            else:
                name = "Daniel"
            timestamp = self.chat_dict['conversations'][7]['events'][i]['timestamp']
            text = ""
            # formatting nonsense
            len_msg = len(self.chat_dict['conversations'][7]['events'][i]['chat_message']['message_content']['segment'])
            segment_list = []
            for j in range(len(self.chat_dict['conversations'][7]['events'][i]['chat_message']['message_content']['segment'])):
                temp_text = self.chat_dict['conversations'][7]['events'][i]['chat_message']['message_content']['segment'][j]['text']
                if temp_text != " " and temp_text != "\n":
                    segment_list.append(j)
            for j in segment_list:
                temp_text = self.chat_dict['conversations'][7]['events'][i]['chat_message']['message_content']['segment'][j]['text']
                if len(segment_list) != 1:
                    if j == 0:
                        text = text + temp_text + "\n"
                    elif j == len_msg-1:
                        text = text + "\t\t" + temp_text
                    else:
                        text = text + "\t\t" + temp_text + "\n"
                else:
                    text = temp_text
                # else:
                #     len_msg = len_msg-1
            msg = self.Message(timestamp, name, text)

            added = False
            for j in range(1, len(self.texts)):
                # if i == 2000:
                # print("message " + str(j) + "/" + str(len(self.texts)))
                if msg.timestamp < self.texts[j].timestamp:
                    self.texts.insert(j-1, msg)
                    added = True
                    break

            # diagnostic message
            if i % 100 == 0:
                print("message " + str(i) + "/" + str(length))
            if added is False:
                self.texts.append(msg)

    def to_txt(self, filename):
        file = open(filename, "w")
        file.write("2710 Chats - 1 Year")
        for i in range(len(self.texts)):
            file.write(self.texts[i].to_string())
        file.close()

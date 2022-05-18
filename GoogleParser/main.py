from parser import ChatParser

if __name__=="__main__":

    # ...
    my_str = ChatParser("Hangouts.json")
    my_str.load_chat()
    my_str.to_txt("may14-2022.txt")
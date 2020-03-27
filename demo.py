with open('words.txt', 'r', encoding='utf-8') as lex:
    lemmata = [line.rstrip('\n') for line in lex.readlines()]
    

    
print(len(lemmata))
        
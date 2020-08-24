#need to fixup the quotes.txt file, the " (quotation marks) are different than input ones
#and some quotes have a , at the end of them ---- dunno how to fix just gonna manually remove them

list_f = [] #final list

with open('quotes.txt', 'r') as file:
    list_i = [] #inital list
    for line in file:
        list_i.append(line)

    for quote in list_i:
        temp = quote.replace('    ', ' _ ')
        temp = temp.replace(temp[0], '"')
        temp1 = temp.split('_')
        curr_quote = temp1[0]
        xd = curr_quote.replace(curr_quote[len(curr_quote) -2], '"')
        temp1[0] = xd
        final = '_'.join(temp1)

        list_f.append(final)

#print(list_f)

with open('quotes_fixed.txt', 'w') as file:
    text = ''.join(list_f)
    file.write(text)
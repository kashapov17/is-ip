#!/bin/bash
#usage: ./test.sh path-to-hillpher.py

function textgen {
    randomtext=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w $(shuf -i 1-20 -n 1) | head -1)
    if [[ randomtext == "" ]]; then
        textgen
    fi
    echo $randomtext
}

for i in {1..100}
    do
    #генерируем ключ
    key=$(textgen)
    #генерируем плэйнтекст
    text=$(textgen)
    #шифруем плэйнтекст
    chiphertext=$(./$1 -k "$key" -t "$text" | sed 's/^.//;s/.$//')

    if [[ $? == 129 ]]; then
        #wooops, детерминант ключевой матрицы, помимо единицы, имеет другие делители с размером алфавита. Обратный элемент в кольце вычетов по модулю $len(alph) не существует!
        echo "$i: bad key was generated ($key)"
        continue
    fi
    #дешифруем полученный шифротекст
    plaintext=$(./$1 -k "$key" -c "$chiphertext" | sed 's/^.//;s/.$//' | xargs)
    if [[ $plaintext == $text ]]; then
        echo "$i:'$text' -> '$chiphertext' -> '$plaintext' with '$key' key is OK"
    else
        echo "$i:'$text' -> '$chiphertext' -> '$plaintext' with '$key' key is WRONG"
    fi
    done

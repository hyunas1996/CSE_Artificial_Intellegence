from collections import defaultdict
import math
import time


#리뷰 파일을 열어서 list에 리뷰를 담는 함수
def getReviews(filename):
    reviews = []

    #encoding issue 처리
    tmp = open(filename, 'r', encoding="UTF-8")

    for line in tmp:
        # 첫 줄 제외하고 reviews 리스트에 리뷰 담기
        if not line.startswith('id'):
            reviews.append(line)

    return reviews

#리뷰 list를 분류기에 넣기 전에 긍정/부정 sorting 작업을 위한 함수
def sortReviews(reviews):
    tempgoodReviews = []
    tempbadReviews = []

    goodReviews = []
    badReviews = []

    for review in reviews:
        line = review.split()

        if line[-1] == '1':
            tempgoodReviews.append(line[1: len(line)-1])

        elif line[-1] == '0':
            tempbadReviews.append(line)

    for line in tempgoodReviews:
        for word in line:
            goodReviews.append(word)

    for line in tempbadReviews:
        for word in line:
            badReviews.append(word)

    return goodReviews, badReviews

#긍정/부정 각각 어떤 단어들이 몇 번 등장하는지 개수 체크하는 함수 >> 리스트 요소 형태 (단어, 긍정 수, 부정 수)
def makeCount(reviews):
    '''
    print("디버깅1: getReviews")
    counts = []

    total_words = totalWords(goodReviews, badReviews)
    print("디버깅2")

    for word in total_words:
        num_good = goodReviews.count(word)
        num_bad = badReviews.count(word)

        counts.append((word, num_good, num_bad))

    print("디버깅3: getReviews 끝")
    return counts
    '''
    print("디버깅 1 : makeCount")
    counts = defaultdict(lambda: [0, 0])

    for i in range(len(reviews)):
        if reviews[i] in counts:
            counts[reviews[i]] += 1
        else:
            counts[reviews[i]] = 1
    print("디버깅 2: makeCount 끝")
    # counts = list(counts.items())
    return counts

#전체 단어를 중복 하는 것을 하나로 표현한 리스트 반환하는 함수
def totalWords(goodReviews, badReviews):
    return list(set(goodReviews + badReviews))

#리뷰의 단어 개수 체크한 결과를 확률로 바꿔주는 함수
def makePossibility(good_count, bad_count, goodReviews, badReviews):
    #긍정 단어 수
    num_good_words = len(goodReviews)
    #부정 단어 수
    num_bad_words = len(badReviews)
    '''
    #good word list
    good_word_list = list(good_count.keys())
    #bad word list
    bad_word_list = list(bad_count.keys())
    '''
    #전체 단어
    total_word = list(set(goodReviews + badReviews))
    #전체 단어 수
    num_total_words = len(total_word)

    #P(긍정)
    total_goodP = num_good_words/num_total_words
    #P(부정)
    total_badP = num_bad_words/num_total_words

    possibility = defaultdict(lambda: [0, 0])

    print("디버깅 3 : makePossibility")
    #print(total)
    for word in total_word:
        if word in good_count:
            #P(word|긍정)
            #goodP = (good_count[word] + 1) / (num_good_words + num_total_words)
            num_good = good_count[word]
        elif word not in good_count:
            #goodP = 1 / (num_good_words + num_total_words)
            num_good = 0

        if word in bad_count:
            #P(word|부정)
            #badP = (bad_count[word] + 1) / (num_bad_words + num_total_words)
            num_bad = bad_count[word]
        elif word not in bad_count:
            #badP = 1 / (num_bad_words + num_total_words)
            num_bad = 0

        goodP = (num_good + 1) / (num_good_words + num_total_words)
        badP = (num_bad + 1) / (num_bad_words + num_total_words)
        possibility[word] = [goodP, badP]

    print("디버깅 4 : makePossibility 끝")
    return possibility, total_goodP, total_badP

#트레이닝 데이터 셋을 통해 학습 후 확률에 대한 표를 반환하는 함수 : possibility와 순서가 동일한 단어모음 리스트 반환
def training():
    origin_reviews = getReviews('ratings_train.txt')
    goodReviews, badReviews = sortReviews(origin_reviews)

    good_count = makeCount(goodReviews)
    bad_count = makeCount(badReviews)
    #print(good_count)
    #print(goodReviews)
    #print(bad_count)
    #print(badReviews)

    possibility, total_goodP, total_badP = makePossibility(good_count, bad_count, goodReviews, badReviews)
    #print(possibility)
    #print(total_goodP)
    #print(total_badP)

    #print(possibility[word_only.index('할')][1])
    #print(possibility[word_only.index('할')][2])

    #print(word_only)
    return possibility, total_goodP, total_badP

#새로운 리뷰에 대해서 긍정인지 부정인지 판단해주는 함수
def classify(possibility, total_goodP, total_badP, newReview):

    newWords = list(newReview.split())
    log_goodP = 0.0
    log_badP = 0.0

    #이방법 개빨라
    for word in newWords:
        if word in possibility:
            value = possibility[word]
            log_goodP += math.log(value[0])
            log_badP += math.log(value[1])
        elif word not in possibility:
            log_goodP += math.log(0.829)
            log_badP += math.log(0.9)

    goodP = log_goodP + math.log(total_goodP)
    badP = log_badP + math.log(total_badP)

    if goodP > badP:
        if exceptions('안', '좋', newReview) == 0:
            return 0
        if exceptions('별로', '좋', newReview) == 0:
            return 0
        if exceptions('안', '재미', newReview) == 0:
            return 0
        if exceptions('별로', '재미', newReview) == 0:
            return 0
        if exceptions('별로', '재밌', newReview) == 0:
            return 0
        if exceptions('안', '재밌', newReview) == 0:
            return 0
        if exceptions('재미', '없', newReview) == 0:
            return 0
        if exceptions('생각보다', '별로', newReview) == 0:
            return 0

        return 1

    else:
        if exceptions('생각보다', '괜찮', newReview) == 0:
            return 1
        if exceptions('기대보다', '괜찮', newReview) == 0:
            return 1

        return 0

    '''

    possibility_list = possibility.keys()
    for word in possibility_list:
        value = possibility[word]
        if word in newWords:
            log_goodP += math.log(value[0])
            log_badP += math.log(value[1])
        else:
            log_goodP += math.log(1-value[0])
            log_badP += math.log(1-value[1])

    goodP = math.exp(log_goodP)
    badP = math.exp(log_badP)

    if goodP > badP:
        result = 1
    else:
        result = 0

    return result
'''

def exceptions(nope, fun, newReview):
    flag = 2
    if fun in newReview:
        index_fun = newReview.find(fun)
        if nope in newReview:
            index_nope = newReview.find(nope)

            if index_fun > index_nope:
                flag = 0
            else:
                flag = 1

    return flag


#새로운 리뷰 파일을 받아와서 classify 결과를 포함한 txt file을 반환하는 함수
def applyNewReview(possibility, total_goodP, total_badP, newFileName):
    resultFile = open('ratings_result_valid.txt', 'w', encoding="UTF-8")
    newReviewFile = open(newFileName, 'r', encoding="UTF-8")

    for line in newReviewFile:
        if line.startswith('id'):
            resultFile.write(line)
        else:
            result = classify(possibility, total_goodP, total_badP, line)
            resultFile.write(line.rstrip('\n') + '    ' + str(result) + '\n')


if __name__ == '__main__':

    start = time.time()

    possibility, total_goodP, total_badP = training()

    applyNewReview(possibility, total_goodP, total_badP, 'ratings_test.txt')

    print("time :", time.time() - start)  # 현재시각 - 시작시간 = 실행 시간


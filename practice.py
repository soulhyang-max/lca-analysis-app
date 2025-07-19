def order(shot=2, size='regular', takeout=False):
    print(f'아메리카노 {size}사이즈 {shot}샷')
    if takeout:
        print('포장주문이 완료되었습니다')
    else:
        print('주문이 완료되었습니다')

order('regular')







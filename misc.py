import pandas as pd
import numpy as np

def rearrange(file):
    pd.set_option('display.max_columns', None)
    coupang_fee = 0.1056
    coupang_extra_fee = 0.033 
    tmon_fee = 0.14 #임시
    tmon_fee_open = -0.08
    ohouse_fee = 0.15 #임시
    ohouse_special_price_fee = -0.05
    filepath = './data/user_upload/{}'.format(file)
    #시간은 2022-03-01 00:07:34 형식으로 기입
    시작시간 = '2022-07-01 15:00:00'
    마감시간 = '2022-07-02 15:00:00'

    naver_new = pd.read_excel(filepath, sheet_name = '네이버 신버전')
    naver_new['판매채널'] = '네이버'
    naver_new['영문명'] = 'naver'
    naver_new = naver_new[["판매채널", "옵션관리코드", "결제일", "주문번호", "택배사", "송장번호", "수량", "상품가격", "옵션가격", "상품별 할인액", "판매자 부담 할인액", "상품별 총 주문금액", "네이버페이 주문관리 수수료", "매출연동 수수료", "정산예정금액","구매자명","수취인명","수취인연락처1","수취인연락처2","우편번호","통합배송지","배송메세지","주문번호","상품명","영문명"]]
    naver_new_dict = {'옵션관리코드': '상품코드','결제일':'결제날짜','상품별 할인액':'상품별할인액', '판매자 부담 할인액':'판매자부담할인액','상품별 총 주문금액':'총주문금액','네이버페이 주문관리 수수료':'결제수수료','매출연동 수수료':'기타수수료','정산예정금액':'정산금액','구매자명':'주문자','수취인명':'받는분','수취인연락처1':'전화번호1','수취인연락처2':'전화번호2','통합배송지':'주소1','상품명':'판매상품명'}
    naver_new.rename(columns = naver_new_dict, inplace = True)
    # naver['결제수수료'] = naver['결제수수료'] * -1 #네이버는 수수료가 음수로 표현된다.
    # naver['기타수수료'] = naver['기타수수료'] * -1 #위와 같은 이유

    coupang = pd.read_excel(filepath, sheet_name = '쿠팡')
    coupang['판매채널'] = '쿠팡'
    coupang['영문명'] = 'coupang'
    coupang['결제수수료'] = coupang['결제액'] * coupang_fee
    coupang['기타수수료'] = coupang['결제액'] * coupang_extra_fee
    coupang['정산금액'] = coupang['결제액'] - coupang['결제수수료'] - coupang['기타수수료']
    coupang['전화번호2'] = ''
    coupang['상품가격'] = ''
    coupang['옵션가격'] = ''
    coupang['상품별할인액'] = ''
    coupang['판매자부담할인액'] = ''
    coupang = coupang[['판매채널' ,'업체상품코드', '주문일', '주문번호', '택배사', '운송장번호', '구매수(수량)','상품가격','옵션가격','상품별할인액','판매자부담할인액', '결제액', '결제수수료', '기타수수료', '정산금액','구매자','수취인이름','수취인전화번호','전화번호2','우편번호','수취인 주소','배송메세지','주문번호','노출상품명(옵션명)','영문명']]
    coupang_dict = {'업체상품코드':'상품코드', '주문일':'결제날짜', '운송장번호':'송장번호', '구매수(수량)':'수량', '결제액':'총주문금액', '구매자':'주문자','수취인이름':'받는분','수취인전화번호':'전화번호1','수취인 주소':'주소1','노출상품명(옵션명)':'판매상품명'}
    coupang.rename(columns = coupang_dict, inplace = True)

    st11 = pd.read_excel(filepath, sheet_name = '11번가')
    st11.fillna(0)
    st11 = st11.replace(',','', regex=True)
    st11_convert = {'판매자기본할인금액': float, '판매자 추가할인금액': float}
    st11 = st11.astype(st11_convert)
    st11['판매채널'] = '11번가'
    st11['영문명'] = '11st'
    st11['상품별할인액'] = st11['복수구매할인금액'] + st11['전고객할인금액']
    st11['판매자부담할인액'] = st11['판매자기본할인금액'] + st11['판매자 추가할인금액']
    st11['전화번호2'] = ''
    st11['기타수수료'] = ''
    st11 = st11[['판매채널','바코드','결제일시','주문번호','택배사코드','송장번호','수량','판매단가','옵션가','상품별할인액','판매자부담할인액','주문금액','서비스이용료','기타수수료','정산예정금액','구매자','수취인','휴대폰번호','전화번호2','우편번호','주소','배송메시지','주문번호','상품명','영문명']]
    st11_dict = {'바코드':'상품코드','결제일시':'결제날짜','택배사코드':'택배사','판매단가':'상품가격','옵션가':'옵션가격','주문금액':'총주문금액','서비스이용료':'결제수수료','정산예정금액':'정산금액','구매자':'주문자','수취인':'받는분','휴대폰번호':'전화번호1','주소':'주소1','배송메시지':'배송메세지','상품명':'판매상품명'}
    st11.rename(columns = st11_dict, inplace = True)

    print("데이터 읽기 완료")

    total = pd.concat([naver_new, coupang, st11], axis = 0)
    total['결제날짜'] = total['결제날짜'].astype('datetime64')
    total['총주문금액'] = total['총주문금액'].astype(float)
    total['정산금액'] = total.정산금액.replace({",":""}, regex=True)
    total['정산금액'] = total['정산금액'].astype(float)
    # total = total.fillna('')
    # total['우편번호'] = pd.to_numeric(total['우편번호'])
    # total['우편번호'] = total['우편번호'].astype(str)
    # total['우편번호'] = total.우편번호.replace({'.0':''}, regex=True)
    total['년도'] = total['결제날짜'].dt.year
    total['월'] = total['결제날짜'].dt.month
    total['상품고유코드'] = total['영문명'] + '-' + total['상품코드']
    total['관리메모1'] = total['판매채널']
    total['배송방식'] = '택배'
    total['주소2'] = ''

    nosnos = total.loc[(total['결제날짜'] >= 시작시간) & (total['결제날짜'] < 마감시간)]
    nosnos_final = nosnos[['결제날짜','상품고유코드','판매상품명','수량','배송방식','주문자','받는분','전화번호1','전화번호2','우편번호','주소1','주소2','배송메세지','주문번호','관리메모1']]
    nosnos_final_order = nosnos_final.sort_values('결제날짜')
    nosnos_final_order['주문번호'] = nosnos_final_order['주문번호'].astype(str)
    nosnos_final_order['우편번호'] = nosnos_final_order['우편번호'].astype(int)
    nosnos_final_order['우편번호'] = nosnos_final_order['우편번호'].astype(str)
    nosnos_final_order['우편번호'] = nosnos_final_order['우편번호'].str.zfill(5)
    nosnos_final_order = nosnos_final_order[['결제날짜','상품고유코드','판매상품명','수량','배송방식','주문자','받는분','전화번호1','전화번호2','우편번호','주소1','주소2','배송메세지','주문번호','관리메모1']]

    채널별_정산 = total.groupby(['월','판매채널'])['총주문금액','정산금액'].apply(lambda x : x.astype(float).sum())

    채널별_판매수량 = total.groupby(['월','판매채널','상품코드'])['수량'].apply(lambda x : x.astype(int).sum()).to_frame()

    total.to_excel("./data/outputs/{}_base_file.xlsx".format(file))
    nosnos_final_order.to_excel("./data/outputs/{}_택배사_양식.xlsx".format(file))
    # 채널별_정산.to_excel('채널별_정산_221116.xlsx')
    # 채널별_판매수량.to_excel("채널별_판매수량_221116.xlsx")
                        

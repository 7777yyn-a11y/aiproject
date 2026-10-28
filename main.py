import streamlit as st
st.title('나의 첫 웹 서비스 만들기!')
a=st.text_input('이름을 입력하셈~')
b=st.selectbox('좋아하는 음식을 선택해라!!',['피자','치킨','떡볶이'])
if st.button('인사말 생성'):
  st.write('방가방가!')
  st.info(a+'님, 반갑습니다!')
  st.warning(b+'를 좋아하시는구나ㅋ')
  st.error('잘부탁한다귀요미')
  st.balloons()
  

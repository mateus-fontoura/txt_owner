import streamlit as st
import hashlib
import dns.resolver

#pip install streamlit
#pip install dnspython
#pip install hashlib

def generate_hash(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()

def check_domain_ownership(domain: str, expected_hash: str) -> bool:
    try:
        txt_records = dns.resolver.resolve(domain, 'TXT')
        for txt_record in txt_records:
            if expected_hash in txt_record.strings[0].decode():
                return True
        return False
    except:
        st.write(f"Não foi possível verificar o domínio: {domain}")
        return False

st.title('Verificador de Propriedade de Domínio')

text_to_hash = st.text_input('Texto para gerar hash:')
domain_to_check = st.text_input('Domínio para verificar:')
check_button_clicked = st.button('Verificar Domínio')

if check_button_clicked and domain_to_check and text_to_hash:
    hash_value = generate_hash(text_to_hash)
    st.write(f'Hash gerado: {hash_value}')
    
    ownership = check_domain_ownership(domain_to_check, hash_value)
    if ownership:
        st.write(f'O domínio {domain_to_check} passou na verificação de propriedade.')
    else:
        st.write(f'O domínio {domain_to_check} não passou na verificação de propriedade.')

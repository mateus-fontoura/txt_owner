import streamlit as st
import dns.resolver
import hashlib

st.title("Verificação de Propriedade de Domínio")

st.subheader("Gerar hash de verificação")
text = st.text_input("Entre com o texto")

# Inicializa hex_dig que é onde gera a Hash em sha256
if "hex_dig" not in st.session_state:
    st.session_state.hex_dig = None

if st.button("Gerar Hash"):
    hash_object = hashlib.sha256(text.encode())
    st.session_state.hex_dig = hash_object.hexdigest()
    st.write(st.session_state.hex_dig)

st.subheader("Verificar domínios")
domains = st.text_area("Entre com os domínios (um por linha)")

if st.button("Verificar Domínios"):
    if st.session_state.hex_dig is None:
        st.error("Por favor, gere uma hash primeiro.")
    else:
        domains = domains.split("\n")  # Dividir por nova linha pra poder verificar varios domains de uma vez
        for domain in domains:
            try:
                answers = dns.resolver.resolve(domain, 'TXT')
                for rdata in answers:
                    for txt_string in rdata.strings:
                        if st.session_state.hex_dig in txt_string.decode():
                            st.success(f"A hash foi encontrada no domínio: {domain}")
                            break
                    else:
                        continue
                    break
                else:
                    st.error(f"A hash não foi encontrada no domínio: {domain}")
            except:
                st.error(f"Não foi possível verificar o domínio: {domain}")

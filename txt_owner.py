import streamlit as st
import dns.resolver
import hashlib
import re
import streamlit.components.v1 as components

st.markdown("""
    <style>
        .reportview-container {
            background-color: #f0f2f6;
        }
        h1, h2 {
            color: #2c3e50;
        }
        .stButton>button {
            background-color: #3498db;
        }
    </style>
    """, unsafe_allow_html=True)

# Função para verificar o domínio
def check_domain(domain, hash_value):
    try:
        answers = dns.resolver.resolve(domain, 'TXT')
        for rdata in answers:
            for txt_string in rdata.strings:
                if hash_value in txt_string.decode():
                    return f"✅ {domain}"
        return f"❌ {domain}"
    except:
        return f"⚠️ {domain}"

# Interface de usuário
st.title("Verificação de Propriedade de Domínio")

# Dividindo em etapas
st.subheader("Etapa 1: Gerar hash de verificação")

# Cria colunas
col1, col2 = st.columns(2)

# Campos de entrada side by side
ticket_id = col1.text_input("Ticket ID (5 dígitos numéricos)", placeholder="Ex.: 12345")
domain = col2.text_input("Domínio(primeiro, se multiplos", placeholder="Ex.: examplo.com")

# Verifica se o Ticket ID é válido
if ticket_id and not re.fullmatch(r'\d{5}', ticket_id):
    st.error("Ticket ID deve conter exatamente 5 dígitos numéricos.")
    st.stop()

# Verifica se o domínio é válido
if domain and not re.fullmatch(r'^[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', domain):
    st.error("Por favor, insira um domínio válido.")
    st.stop()

# Concatena o Ticket ID e o domínio para gerar o hash
text_to_hash = ticket_id + domain

if st.button("Gerar Hash") and ticket_id and domain:
    hash_object = hashlib.sha256(text_to_hash.encode())
    st.session_state.hex_dig = hash_object.hexdigest()
    st.success(f"✅ Hash gerada com sucesso: {st.session_state.hex_dig}")

st.subheader("Etapa 2: Verificar domínios")
domains = st.text_area("Entre com os domínios (um por linha)")


if st.session_state.get('hex_dig'):
    st.markdown(f"🔒 Hash atual: `{st.session_state.hex_dig}`")



#https://dns.google/resolve?name={domain}&type=TXT


# Organiza os botões em colunas
button_col1, button_col2, button_col3 = st.columns(3)

# Botão para verificar os domínios
if button_col1.button("Verificar domínios"):
    if not st.session_state.get('hex_dig'):
        st.error("Por favor, gere uma hash primeiro.")
    else:
        domains = domains.split("\n")
        results_col1, results_col2 = st.columns(2)
        
        with st.spinner('Verificando domínios...'):
            for i, domain in enumerate(domains):
                if domain.strip() == '':
                    continue
                result = check_domain(domain.strip(), st.session_state.get('hex_dig'))
                if i % 2 == 0:
                    results_col1.write(result)
                else:
                    results_col2.write(result)
        st.success('Verificação concluída!')

# Botão para exportar o Curl
if button_col2.button('Exportar Curl'):
    if 'hex_dig' in st.session_state and domain:
        # Códigos de escape ANSI para cores
        green = '\\033[32m'
        red = '\\033[31m'
        reset = '\\033[0m'

        # Linha de caracteres com tamanho fixo
        line = '=' * 40

        # Cria o comando curl em uma única linha com cores e formatação aprimorada
        curl_command = (
            'clear && '  # Limpa a tela do terminal
            f'curl --silent "https://dns.google/resolve?name={domain}&type=TXT" | '
            f'grep "{st.session_state.hex_dig}" > /dev/null && '
            f'echo "\\n{green}{line}\\nHash encontrada: {st.session_state.hex_dig}\\n{line}{reset}\\n" || '
            f'echo "\\n{red}{line}\\nHash não encontrada\\n{line}{reset}\\n"'
        )

        # HTML para criar uma caixa com o comando curl e um botão de copiar
        copy_box_html = f'''
        <div style="position: relative; white-space: pre-wrap; overflow-x: auto; border: 1px solid #ccc; padding: 10px;">
            <code id="curlCommand">{curl_command}</code>
            <button onclick="copyCurl()" style="position: absolute; right: 10px; top: 10px;">Copiar</button>
        </div>
        <script>
            function copyCurl() {{
                var textArea = document.createElement('textarea');
                textArea.value = document.getElementById('curlCommand').textContent;
                document.body.appendChild(textArea);
                textArea.select();
                document.execCommand('copy');
                document.body.removeChild(textArea);
                alert('Comando copiado para a área de transferência!');
            }}
        </script>
        '''

        # Imprime a caixa com o botão de copiar
        components.html(copy_box_html, height=100)

# Botão para limpar
if button_col3.button("Limpar"):
    st.session_state.clear()
    st.experimental_rerun()

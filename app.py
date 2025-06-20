from flask import Flask, render_template, request, flash, redirect, url_for
import requests
import os 
from datetime import datetime
import pytz 

app = Flask(__name__)
app.secret_key = os.urandom(24) 

API_KEY = os.getenv('API_KEY', 'SUA CHAVE API AQUI') 

EXCHANGE_RATE_BASE_URL = 'https://v6.exchangerate-api.com/v6/'

# --- DICIONÁRIO DE SÍMBOLOS DE MOEDAS ATUALIZADO ---

CURRENCY_SYMBOLS = {
  "USD": "$",
  "AED": "د.إ", # Dirham dos Emirados Árabes Unidos
  "AFN": "؋", # Afegane Afegão
  "ALL": "Lek", # Lek Albanês
  "AMD": " dram", # Dram Armênio
  "ANG": "ƒ", # Guilder das Antilhas Holandesas
  "AOA": "Kz", # Kwanza Angolano
  "ARS": "$", # Peso Argentino
  "AUD": "A$", # Dólar Australiano
  "AWG": "ƒ", # Florim de Aruba
  "AZN": "₼", # Manat Azerbaijano
  "BAM": "KM", # Marco Conversível da Bósnia e Herzegovina
  "BBD": "$", # Dólar de Barbados
  "BDT": "৳", # Taka de Bangladesh
  "BGN": "лв", # Lev Búlgaro
  "BHD": ".د.ب", # Dinar do Bahrein
  "BIF": "FBu", # Franco Burundinês
  "BMD": "$", # Dólar das Bermudas
  "BND": "$", # Dólar do Brunei
  "BOB": "Bs.", # Boliviano Boliviano
  "BRL": "R$", # Real Brasileiro
  "BSD": "$", # Dólar das Bahamas
  "BTN": "Nu.", # Ngultrum Butanês
  "BWP": "P", # Pula Botsuanesa
  "BYN": "Br", # Rublo Bielorrusso
  "BZD": "BZ$", # Dólar de Belize
  "CAD": "C$", # Dólar Canadense
  "CDF": "FC", # Franco Congolês
  "CHF": "CHF", # Franco Suíço
  "CLP": "$", # Peso Chileno
  "CNY": "¥", # Yuan Chinês
  "COP": "$", # Peso Colombiano
  "CRC": "₡", # Colón Costarriquenho
  "CUP": "$", # Peso Cubano
  "CVE": "Esc", # Escudo Cabo-verdiano
  "CZK": "Kč", # Coroa Checa
  "DJF": "Fdj", # Franco do Djibuti
  "DKK": "kr", # Coroa Dinamarquesa
  "DOP": "RD$", # Peso Dominicano
  "DZD": "دج", # Dinar Argelino
  "EGP": "E£", # Libra Egípcia
  "ERN": "Nfk", # Nakfa Eritreia
  "ETB": "Br", # Birr Etíope
  "EUR": "€", # Euro
  "FJD": "FJ$", # Dólar de Fiji
  "FKP": "£", # Libra das Ilhas Malvinas
  "FOK": "kr", # Coroa Faroesa
  "GBP": "£", # Libra Esterlina
  "GEL": "₾", # Lari Georgiano
  "GGP": "£", # Libra de Guernsey
  "GHS": "₵", # Cedi Ganês
  "GIP": "£", # Libra de Gibraltar
  "GMD": "D", # Dalasi Gambiano
  "GNF": "FG", # Franco Guineense
  "GTQ": "Q", # Quetzal Guatemalteco
  "GYD": "GY$", # Dólar da Guiana
  "HKD": "HK$", # Dólar de Hong Kong
  "HNL": "L", # Lempira Hondurenha
  "HRK": "kn", # Kuna Croata (agora é Euro)
  "HTG": "G", # Gourde Haitiano
  "HUF": "Ft", # Forint Húngaro
  "IDR": "Rp", # Rupia Indonésia
  "ILS": "₪", # Novo Shekel Israelense
  "IMP": "£", # Libra da Ilha de Man
  "INR": "₹", # Rúpia Indiana
  "IQD": "ع.د", # Dinar Iraquiano
  "IRR": "﷼", # Rial Iraniano
  "ISK": "kr", # Coroa Islandesa
  "JEP": "£", # Libra de Jersey
  "JMD": "J$", # Dólar Jamaicano
  "JOD": "JD", # Dinar Jordaniano
  "JPY": "¥", # Iene Japonês
  "KES": "KSh", # Xelim Queniano
  "KGS": "с", # Som Quirguiz
  "KHR": "៛", # Riel Cambojano
  "KID": "$", # Dólar de Kiribati
  "KMF": "CF", # Franco Comoriano
  "KRW": "₩", # Won Sul-Coreano
  "KWD": "KD", # Dinar Kuwaitiano
  "KYD": "$", # Dólar das Ilhas Cayman
  "KZT": "₸", # Tenge Cazaque
  "LAK": "₭", # Kip Laosiano
  "LBP": "ل.ل", # Libra Libanesa
  "LKR": "Rs", # Rúpia do Sri Lanka
  "LRD": "$", # Dólar Liberiano
  "LSL": "L", # Loti Lesoto
  "LYD": "LD", # Dinar Líbio
  "MAD": "د.م.", # Dirham Marroquino
  "MDL": "L", # Leu Moldávio
  "MGA": "Ar", # Ariary Malgaxe
  "MKD": "ден", # Denar Macedônio
  "MMK": "Ks", # Kyat de Mianmar
  "MNT": "₮", # Tögrög Mongol
  "MOP": "P", # Pataca de Macau
  "MRU": "UM", # Ouguiya Mauritana
  "MUR": "₨", # Rúpia Mauriciana
  "MVR": "Rf", # Rufiyaa Maldiva
  "MWK": "MK", # Kwacha Malauiana
  "MXN": "$", # Peso Mexicano
  "MYR": "RM", # Ringgit Malaio
  "MZN": "MT", # Metical Moçambicano
  "NAD": "N$", # Dólar Namíbio
  "NGN": "₦", # Naira Nigeriana
  "NIO": "C$", # Córdoba Nicaraguense
  "NOK": "kr", # Coroa Norueguesa
  "NPR": "₨", # Rúpia Nepalesa
  "NZD": "NZ$", # Dólar Neozelandês
  "OMR": "ر.ع.", # Rial Omanense
  "PAB": "B/.", # Balboa Panamenho
  "PEN": "S/.", # Sol Peruano
  "PGK": "K", # Kina da Papua Nova Guiné
  "PHP": "₱", # Peso Filipino
  "PKR": "₨", # Rúpia Paquistanesa
  "PLN": "zł", # Zloty Polonês
  "PYG": "₲", # Guarani Paraguaio
  "QAR": "ر.ق", # Rial Catarense
  "RON": "lei", # Leu Romeno
  "RSD": "дин", # Dinar Sérvio
  "RUB": "₽", # Rublo Russo
  "RWF": "Fr", # Franco Ruandês
  "SAR": "ر.س", # Rial Saudita
  "SBD": "$", # Dólar das Ilhas Salomão
  "SCR": "₨", # Rúpia das Seicheles
  "SDG": "ج.س.", # Libra Sudanesa
  "SEK": "kr", # Coroa Sueca
  "SGD": "S$", # Dólar de Singapura
  "SHP": "£", # Libra de Santa Helena
  "SLE": "Le", # Leone de Serra Leoa
  "SLL": "Le", # Leone de Serra Leoa
  "SOS": "Sh", # Xelim Somali
  "SRD": "$", # Dólar Surinamês
  "SSP": "£", # Libra Sul-Sudanesa
  "STN": "Db", # Dobra de São Tomé e Príncipe
  "SYP": "£", # Libra Síria
  "SZL": "E", # Lilangeni Suazi
  "THB": "฿", # Baht Tailandês
  "TJS": "SM", # Somoni Tajique
  "TMT": "m", # Manat Turcomeno
  "TND": "د.ت", # Dinar Tunisiano
  "TOP": "T$", # Paʻanga de Tonga
  "TRY": "₺", # Lira Turca
  "TTD": "TT$", # Dólar de Trinidad e Tobago
  "TVD": "$", # Dólar de Tuvalu
  "TWD": "NT$", # Novo Dólar Taiwanês
  "TZS": "Sh", # Xelim da Tanzânia
  "UAH": "₴", # Hryvnia Ucraniana
  "UGX": "USh", # Xelim Ugandense
  "UYU": "$U", # Peso Uruguaio
  "UZS": "сум", # Som Uzbeque
  "VES": "Bs", # Bolívar Soberano Venezuelano
  "VND": "₫", # Dong Vietnamita
  "VUV": "Vt", # Vatu de Vanuatu
  "WST": "WS$", # Tala Samoana
  "XAF": "FCFA", # Franco CFA da África Central
  "XCD": "$", # Dólar do Caribe Oriental
  "XCG": "$", # Dólar do Caribe Oriental (repetição)
  "XDR": "SDR", # Direitos Especiais de Saque (geralmente não tem símbolo monetário simples)
  "XOF": "FCFA", # Franco CFA da África Ocidental
  "XPF": "₣", # Franco CFP
  "YER": "﷼", # Rial Iemenita
  "ZAR": "R", # Rand Sul-Africano
  "ZMW": "K", # Kwacha Zambiana
  "ZWL": "Z$" # Dólar Zimbabuense
}
# --- FIM DO DICIONÁRIO ATUALIZADO ---

def get_supported_currencies():
    url = f"{EXCHANGE_RATE_BASE_URL}{API_KEY}/codes"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        if data.get('result') == 'success' and 'supported_codes' in data:
            currencies = {code: name for code, name in data['supported_codes']}
            return currencies
        else:
            print(f"Erro ao obter lista de moedas da API: {data.get('error-type', 'Erro desconhecido')}")
            return {}
    except requests.exceptions.RequestException as e:
        print(f"Erro de conexão ao obter lista de moedas: {e}")
        return {}
    except Exception as e:
        print(f"Erro inesperado ao obter lista de moedas: {e}")
        return {}

@app.route('/', methods=['GET', 'POST'])
def home():
    currencies = get_supported_currencies()
    if not currencies:
        flash('Não foi possível carregar a lista de moedas. Tente novamente mais tarde ou verifique sua chave API.', 'error')

    if request.method == 'POST':
        amount_str = request.form.get('amount')
        from_c = request.form.get('from_c')
        to_c = request.form.get('to_c')

        if not all([amount_str, from_c, to_c]):
            flash('Por favor, preencha todos os campos.', 'error')
            return render_template('home.html', currencies=currencies)

        try:
            amount = float(amount_str)
            if amount <= 0:
                flash('O valor para conversão deve ser positivo.', 'error')
                return render_template('home.html', currencies=currencies)
        except ValueError:
            flash('Valor inválido. Por favor, insira um número.', 'error')
            return render_template('home.html', currencies=currencies)

        try:
            url = f"{EXCHANGE_RATE_BASE_URL}{API_KEY}/pair/{from_c}/{to_c}"
            
            response = requests.get(url=url, timeout=10)
            response.raise_for_status() 
            data = response.json()

            if data.get('result') != 'success':
                error_type = data.get('error-type', 'Erro desconhecido na API.')
                flash(f'Erro da API: {error_type}. Verifique os códigos das moedas e sua chave.', 'error')
                return render_template('home.html', currencies=currencies)
            
            rate = float(data.get('conversion_rate'))
            result = rate * amount

            brasilia_timezone = pytz.timezone('America/Sao_Paulo') 

            time_utc_str = data.get('time_last_update_utc', 'N/A')
            
            formatted_time = 'N/A'
            if time_utc_str != 'N/A':
                try:
                    dt_utc = datetime.strptime(time_utc_str, "%a, %d %b %Y %H:%M:%S %z")
                    dt_brasilia = dt_utc.astimezone(brasilia_timezone)
                    formatted_time = dt_brasilia.strftime("%d/%m/%Y %H:%M:%S")
                except ValueError as e:
                    print(f"Erro ao parsear data/hora da API: {e}")
                    formatted_time = 'Formato inválido'

            context_data = {
                'result': round(result, 2),
                'amount': amount,
                'from_c_code': data.get('base_code', 'N/A'),
                'from_c_name': currencies.get(data.get('base_code'), 'N/A'),
                'to_c_code': data.get('target_code', 'N/A'),
                'to_c_name': currencies.get(data.get('target_code'), 'N/A'),
                'time': formatted_time, 
                'currencies': currencies,
                # --- BUSCA OS SÍMBOLOS NO DICIONÁRIO ATUALIZADO ---
                'from_c_symbol': CURRENCY_SYMBOLS.get(data.get('base_code'), ''), 
                'to_c_symbol': CURRENCY_SYMBOLS.get(data.get('target_code'), '')
                # --- FIM DAS VARIÁVEIS ---
            }

            return render_template('home.html', **context_data)

        except requests.exceptions.RequestException as e:
            flash(f'Erro de conexão: Não foi possível conectar à API. Detalhes: {e}', 'error')
            return render_template('home.html', currencies=currencies)
        except (ValueError, TypeError) as e:
            flash('Erro ao processar a taxa de câmbio. Formato inesperado da API ou dados ausentes.', 'error')
            return render_template('home.html', currencies=currencies)
        except Exception as e:
            flash(f'Ocorreu um erro inesperado: {e}', 'error')
            return render_template('home.html', currencies=currencies)

    return render_template('home.html', currencies=currencies, CURRENCY_SYMBOLS=CURRENCY_SYMBOLS)

if __name__ == "__main__":
    app.run(debug=True)

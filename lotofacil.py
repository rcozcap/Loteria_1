import flet as ft
from flet import *
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import pyautogui
import json
from collections import Counter
import locale
import datetime

def main(page: ft.Page):

    page.title = "Loterias"
    page.window_title_bar_hidden = True
    page.theme_mode = ft.ThemeMode.LIGHT

    page.theme = Theme(color_scheme_seed="blue")
    page.update()

    page.dark_theme = Theme(color_scheme_seed="amber")

    page.update()

    page.window.min_width = 500
    page.window.min_height = 600
    page.padding = 10
    page.window.resizable = True
    page.scroll = ft.ScrollMode.AUTO

    normal_radius = 100
    hover_radius = 110
    normal_title_style = ft.TextStyle(
        size=20, color=ft.colors.WHITE, weight=ft.FontWeight.BOLD
    )
    hover_title_style = ft.TextStyle(
        size=32,
        color=ft.colors.WHITE,
        weight=ft.FontWeight.BOLD,
        shadow=ft.BoxShadow(blur_radius=2, color=ft.colors.BLACK54),
    )

    #Função que abre o dialog para confirmar o encerramento do app
    def close_event(e):
        page.dialog = confirm_dialog
        confirm_dialog.open = True
        page.update()

    page.window.prevent_close = True
    #opção sim ou não de encerramento
    def yes_click(e):
        page.window.destroy()

    def no_click(e):
        confirm_dialog.open = False
        page.update()
    #dialog que será aberto para a confirmação do encerramento
    confirm_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Fechar"),
        content=ft.Text("Realmente deseja encerrar a execução do aplicativo?"),
        actions=[
            ft.ElevatedButton("Sim", on_click=yes_click),
            ft.OutlinedButton("Não", on_click=no_click),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )
    #Função que checa se houve o clique para abrir o menu
    def check_item_clicked(e):
        e.control.checked = not e.control.checked
        page.update()

    def theme_mode_switch(e):
        page.theme_mode = (
            ft.ThemeMode.DARK
            if page.theme_mode == ft.ThemeMode.LIGHT
            else ft.ThemeMode.LIGHT
        )

        if page.theme_mode == ft.ThemeMode.LIGHT:
            page.appbar = ft.AppBar(
                leading=ft.Icon(ft.icons.BALLOT_SHARP),
                leading_width=40,
                title=ft.Text("Loterias"),
                center_title=False,
                bgcolor=ft.colors.SURFACE_VARIANT,
                actions=[
                        th_btt(
                        icon = ft.icons.WB_SUNNY_OUTLINED,
                        on_click=theme_mode_switch,
                        tooltip="Alternar para o tema escuro",
                        ),
            ft.IconButton(ft.icons.FILTER_3),
            ft.PopupMenuButton(
                items=[
                    ft.PopupMenuItem(text="Fechar", on_click=close_event),
                    ft.PopupMenuItem(),  # divider
                    #ft.PopupMenuItem(text="Maximizar", on_click=close_event),
                    #    text="Checked item", checked=False, on_click=check_item_clicked
                ]
            ),
        ],
        )
                       
        else:
            page.appbar = ft.AppBar(
                leading=ft.Icon(ft.icons.BALLOT_SHARP),
                leading_width=40,
                title=ft.Text("Loterias"),
                center_title=False,
                bgcolor=ft.colors.SURFACE_VARIANT,
                actions=[
                        th_btt(
                        icon = ft.icons.WB_SUNNY,
                        on_click=theme_mode_switch,
                        tooltip="Alternar para o tema claro",
                       ),
            ft.IconButton(ft.icons.FILTER_3),
            ft.PopupMenuButton(
                items=[
                    ft.PopupMenuItem(text="Fechar", on_click=close_event),
                    ft.PopupMenuItem(),  # divider
                    #ft.PopupMenuItem(text="Maximizar", on_click=close_event),
                    #    text="Checked item", checked=False, on_click=check_item_clicked
                ]
            ),
        ],
        )

        page.update()

    th_btt = ft.IconButton
    
    #barra de opções superior
    page.appbar = ft.AppBar(
        leading=ft.Icon(ft.icons.BALLOT_SHARP),
        leading_width=40,
        title=ft.Text("Loterias"),
        center_title=False,
        bgcolor=ft.colors.SURFACE_VARIANT,
        actions=[
                th_btt(
                icon = ft.icons.WB_SUNNY_OUTLINED,
                on_click=theme_mode_switch,
                tooltip="Alternar para o tema escuro",
                ),
            ft.IconButton(ft.icons.FILTER_3),
            ft.PopupMenuButton(
                items=[
                    ft.PopupMenuItem(text="Fechar", on_click=close_event),
                    ft.PopupMenuItem(),  # divider
                    #ft.PopupMenuItem(text="Maximizar", on_click=close_event),
                        #text="Checked item", checked=False, on_click=check_item_clicked
                ]
            ),
        ],
    )
    #abrir arquivo salvo no computador
    def sheet_values(e: FilePickerResultEvent):
        save_file_dir = ft.Text()
        save_file_dir.value = (
        ", \n".join(map(lambda f: f.path, e.files)) if e.files else "Ao menos um arquivo é obrigatório"
        )
        print(save_file_dir) 
 
        save_file_dir1 = str(save_file_dir).replace("text {'value': '", '')
        save_file_dir2 = str(save_file_dir1).replace("'}", '')
        print(save_file_dir2)

        global save_sheet 
        save_sheet = save_file_dir2   

        page.controls.clear(),

        page.add(
            ft.Column(
                scroll=ft.ScrollMode.AUTO,
                controls=[
                ft.Row(
                [
                ft.Container(
                    ft.ElevatedButton(
                        "Carregar planilha salva",
                        icon=ft.icons.FILE_UPLOAD_OUTLINED,
                        on_click=lambda _: save_file_dialog.pick_files(
                        ),
                    ),
                bgcolor=ft.colors.PRIMARY,
                alignment=ft.alignment.center_left,
                padding=5,
                height=100, 
                ),
                ft.Container(
                ft.Text(save_sheet,
                    color=ft.colors.SECONDARY_CONTAINER,
                    text_align=ft.TextAlign.CENTER,    
                        ),
                bgcolor=ft.colors.PRIMARY,
                alignment=ft.alignment.center,
                padding=5,
                height=100,
                expand=True,
                ),
                ],
                spacing=5,
                ),
                ft.Row(
                    spacing=0,
                    alignment=ft.alignment.center,
                    height=100,
                    controls=[
                    ft.Container(
                        ft.Text("Se houver dados na planilha, o sitema usará o último concurso capturado como "
                                "referência e a busca será feita a partir desse concurso até o último publicado, "
                                "se não houver dados na planilha o sistema abrirá um campo para que digite o número "
                                "do concurso e usará o concurso digitado para fazer uma busca desse número até o "
                                "o último públicado",
                            color=ft.colors.PRIMARY,    
                                ),
                    bgcolor=ft.colors.SECONDARY_CONTAINER,
                    alignment=ft.alignment.center,
                    #width=150,
                    expand=True,
                    ),
                ],
                ),
                ft.Row(
                    spacing=0,
                    alignment=ft.alignment.center,
                    height=100,
                    controls=[    
                    ft.Container(    
                        ft.Text('APÓS CAPTURADOS OS DADOS SERÃO SALVOS NA PLANILHA AUTOMATICAMENTE',
                            color=ft.colors.SECONDARY_CONTAINER,
                            text_align=ft.TextAlign.CENTER,    
                                ),
                        bgcolor=ft.colors.PRIMARY,
                        alignment=ft.alignment.center,
                        padding=5,
                        height=60,
                        expand=True,
                ),
                ],
                ),
                ft.Row(
                [
                ft.Container(
                    ft.ElevatedButton(
                        "Buscar Resultados",
                        icon=ft.icons.START,
                        on_click=(loto_scrap
                        ),
                    ),
                #bgcolor=ft.colors.BLUE_100,
                alignment=ft.alignment.center,
                padding=5,
                height=100,
                expand=True,
                ),
                ],
                spacing=5,
                ),
                ],
            ),
        )
        page.navigation_bar = ft.NavigationBar(
            on_change=data_base,
            destinations=[
                ft.NavigationBarDestination(
                    icon=ft.icons.FILE_COPY_OUTLINED, 
                    selected_icon=ft.icons.FILE_COPY_ROUNDED,
                    label="Arquivo(Carregar/Criar)"
                    ),
                ft.NavigationBarDestination(
                    icon=ft.icons.BALLOT_OUTLINED, 
                    selected_icon=ft.icons.BALLOT_ROUNDED,
                    label="Base de dados"
                    ),
                ft.NavigationBarDestination(
                    icon=ft.icons.TABLE_CHART_OUTLINED,
                    selected_icon=ft.icons.TABLE_CHART,
                    label="BI",
                    ),
                ft.NavigationBarDestination(
                    icon=ft.icons.DATA_EXPLORATION_OUTLINED,
                    selected_icon=ft.icons.DATA_EXPLORATION,
                    label="Insights",
                ),
            ]
        )
        page.update()

    def loto_scrap(e):

        global df
        df = pd.read_excel(save_sheet)

        ft.Column(
                scroll=ft.ScrollMode.AUTO,
                controls=[
                    ft.Row(
                        spacing=0,
                        alignment=ft.alignment.center,
                        height=50,
                        controls = [
                        ft.Container(
                            ft.Text("Data",
                                color=ft.colors.PRIMARY,    
                                    ),
                            bgcolor=ft.colors.SECONDARY_CONTAINER,
                            alignment=ft.alignment.center,
                            width=150,
                            #height=50,
                            #expand=True,
                        ),
                        ft.VerticalDivider(width=3, thickness=3, color="white"),
                        ft.Container(
                            ft.Text("Concurso",
                                color=ft.colors.PRIMARY,    
                                    ),
                            bgcolor=ft.colors.PRIMARY_CONTAINER,
                            alignment=ft.alignment.center,
                            width=150,
                            #height=50,
                            #expand=True,
                        ),
                        ft.VerticalDivider(width=3, thickness=3, color="white"),
                        ft.Container(
                            ft.Text("Numeros Sorteados",
                                    color=ft.colors.PRIMARY,    
                                    ),
                            bgcolor=ft.colors.PRIMARY_CONTAINER,
                            alignment=ft.alignment.center,
                            width=150,
                            #height=50,
                            #expand=True,
                        ),
                        ft.VerticalDivider(width=3, thickness=3, color="white"),
                        ft.Container(
                            ft.Text("Ganhadores",
                                color=ft.colors.PRIMARY,
                                    ),
                            bgcolor=ft.colors.SECONDARY_CONTAINER,
                            alignment=ft.alignment.center,
                            width=150,
                            #height=50,
                            expand=True,
                        ),
                        ft.VerticalDivider(width=3, thickness=3, color="white"),
                        ft.Container(
                            ft.Text("Apostas ganhadoras",
                                color=ft.colors.PRIMARY,    
                                    ),
                            bgcolor=ft.colors.SECONDARY_CONTAINER,
                            alignment=ft.alignment.center,
                            width=150,
                            #height=50,
                            expand=True,
                        ),
                        ft.VerticalDivider(width=3, thickness=3, color="white"),
                        ft.Container(
                            ft.Text("Arrecadação",
                                color=ft.colors.PRIMARY,    
                                    ),
                            bgcolor=ft.colors.PRIMARY_CONTAINER,
                            alignment=ft.alignment.center,
                            width=150,
                            #height=50,
                            #expand=True,
                        ),
                        ft.VerticalDivider(width=3, thickness=3, color="white"),
                        ft.Container(
                            ft.Text("Acumulou?",
                                color=ft.colors.PRIMARY,    
                                    ),
                            bgcolor=ft.colors.PRIMARY_CONTAINER,
                            alignment=ft.alignment.center,
                            width=150,
                            #height=50,
                            #expand=True,
                        ),
                        ],
                    ),
                ],
            ),

        #USAR CONCURSO 3118

        def concurso_get(e):

            df = pd.read_excel(save_sheet)

            #A classe Service é utilizada para criar uma instância do Chrome WebDriver 
            service = Service()

            #webdriver.ChromeOptions é utilizado para definir a preferência para o browser do Chrome
            options = webdriver.ChromeOptions()
            #options.add_argument("--headless=new")

            #Inicia-se a instância do Chrome WebDrive com as classes definidas, service e options 
            driver = webdriver.Chrome(service = service, options = options)

            #URL de onde vamos pegar os dados
            url = 'https://loterias.caixa.gov.br/Paginas/Lotofacil.aspx'
            #headers = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"}

            #Acessando a URL
            driver.get(url)
            time.sleep(2)

            #como encontrar elementos do HTML
            #find_element(By.ID, "id")
            #find_element(By.NAME, "name")
            #find_element(By.XPATH, "xpath")
            #find_element(By.LINK_TEXT, "link text")
            #find_element(By.PARTIAL_LINK_TEXT, "partial link text")
            #find_element(By.TAG_NAME, "tag name")
            #find_element(By.CLASS_NAME, "class name")
            #find_element(By.CSS_SELECTOR, "css selector")

            #buscar textos no HTML
            #td.get_attribute('innerHTML')
            #td.get_attribute('innerText')
            #td.get_attribute('textContent')
            
            #Captura dos dados

            #Capturando a data
            lotofacil_data = driver.find_elements(By.XPATH, "//*[@id='wp_resultados']/div[1]/div/h2/span")[0].text
            #separando a string que contém concurso e data
            Concurso,Data = lotofacil_data.split('(', 1)
            Concurso = Concurso.replace('Concurso ', '')
            #removendo o parenteses da data
            #Data = Data.replace(')', '')
            #Data = datetime.datetime.strptime(Data, '%d/%m/%Y')
            
            ultimo_concurso_salvo = str(input_c.value)
            #ultimo_concurso_salvo = ultimo_concurso_salvo.replace('Concurso ', '')

            #ultima_data_exc = df['Data'].iloc[-1]
            #ultima_data_exc_tratada = datetime.datetime.strptime(ultima_data_exc, '%d/%m/%Y')
            #data_atual = format(datetime.datetime.now(), '%d/%m/%Y')
            #data_atual_tratada = datetime.datetime.strptime(data_atual, '%d/%m/%Y')
            #data_atual_tratada = data_atual_tratada - datetime.timedelta(days=1)
            #diferenca = data_atual_tratada - ultima_data_exc_tratada
            #difference_list = []

            old_concurso = driver.find_element(By.XPATH, "//*[@id='buscaConcurso']").click()

            print(Concurso)
            print(ultimo_concurso_salvo)

            #Se o último concurso salvo na planilha não for igual ao atual no site o sistema voltará e capturará todos os ainda não
            #capturados até o mais atual
            for i in range(int(ultimo_concurso_salvo)+1,int(Concurso)+1):
                
                driver.find_element(By.XPATH, "//*[@id='buscaConcurso']").click
                time.sleep(2)
                driver.find_element(By.XPATH, "//*[@id='buscaConcurso']").send_keys(i)
                time.sleep(2)
                pyautogui.press('ENTER') 
                time.sleep(2)
                pyautogui.press('backspace')
                pyautogui.press('backspace')
                pyautogui.press('backspace')
                pyautogui.press('backspace')
                time.sleep(2)
                #Capturando a data
                lotofacil_data = driver.find_elements(By.XPATH, "//*[@id='wp_resultados']/div[1]/div/h2/span")[0].text
                #Capturando os números sorteados
                lotofacil_numbers = driver.find_elements(By.CSS_SELECTOR, ".ng-binding.dezena.ng-scope")[0:15]
                #Capturando o texto dos números para cada número na lista
                all_lotofacil_numbers = [number.get_attribute('innerText') for number in lotofacil_numbers]
                #Capturando os ganhadores
                lotofacil_ganhadores = driver.find_elements(By.CSS_SELECTOR, ".description.ng-binding.ng-scope")[0:5]
                #Capturando o texto dos números para cada ganhador na lista
                all_lotofacil_winners = [winner.get_attribute('innerText') for winner in lotofacil_ganhadores]
                #Capturando a arrecadação total
                lotofacil_dados_extras = driver.find_elements(By.XPATH, "//div[contains(@class, 'related-box gray-text no-margin')]/p")[6:27]
                #Capturando o texto da arrecadação
                lotofacil_dados_extras_text = [arrecadacao_details.get_attribute('innerText') for arrecadacao_details in lotofacil_dados_extras]


                #Tratamento dos dados
                #separando a string que contém concurso e data
                Concurso,Data = lotofacil_data.split('(', 1)
                #tirando ')' da data
                Data = Data.replace(')','')
                #Transformando o array de números sorteados em string separados por '-'
                loteria_numbers_to_string = ' - '.join(str(x) for x in all_lotofacil_numbers)
                #Transformando o array de ganhadores em string separados por '-'
                loteria_winners_to_string = ' - '.join(str(x) for x in all_lotofacil_winners)
                #Transformando o array que traz a arrecadação e dados extras em string separada por ' '
                lotofacil_dados_extras_text_tratado = ''.join(str(x) for x in lotofacil_dados_extras_text)
                #remove os textos a mais deixando apenas o valor da arrecadação e separa dos dados extras
                detalhamento,arrecadacao = lotofacil_dados_extras_text_tratado.split('R$', 1)
                arrecadacao = arrecadacao.replace(' Veja o detalhamento', '')
                #Saber se houve ganhador ou acumulou
                if 'Não houve acertador' in loteria_winners_to_string: 
                    loteria_acumulou = 'Acumulou!'
                else:
                    loteria_acumulou = 'Houve Ganhador'

                #Transformando todos os dados coletados em um array
                List_data_for_export = [Data,Concurso,loteria_numbers_to_string,loteria_winners_to_string,detalhamento,arrecadacao,loteria_acumulou]

                #print(ultima_data_exc_tratada)
                #print(data_atual_tratada)
                #print(diferenca)
                #print(Data)
                #print(Concurso)
                #print(loteria_numbers_to_string)
                #print(loteria_winners_to_string)
                #print(detalhamento)
                #print(arrecadacao)
                #print(loteria_acumulou)
                #print(List_data_for_export)

                page.add(
                    ft.Column(
                    scroll=ft.ScrollMode.ALWAYS,
                    controls=[
                        ft.Row(
                            spacing=0,
                            alignment=ft.alignment.center,
                            height=350,
                            controls=[
                            ft.Container(
                                ft.Text(List_data_for_export[0],
                                    color=ft.colors.PRIMARY,    
                                        ),
                                bgcolor=ft.colors.SECONDARY_CONTAINER,
                                alignment=ft.alignment.center,
                                width=150,
                                #expand=True,
                            ),
                            ft.VerticalDivider(width=3, thickness=3, color="white"),
                            ft.Container(
                                ft.Text(List_data_for_export[1],
                                    color=ft.colors.PRIMARY,    
                                        ),
                                bgcolor=ft.colors.PRIMARY_CONTAINER,
                                alignment=ft.alignment.center,
                                width=150,
                                #expand=True,
                            ),
                            ft.VerticalDivider(width=3, thickness=3, color="white"),
                            ft.Container(
                                ft.Text(List_data_for_export[2],
                                    color=ft.colors.PRIMARY,    
                                        ),
                                bgcolor=ft.colors.PRIMARY_CONTAINER,
                                alignment=ft.alignment.center,
                                width=150,
                                #expand=True,
                            ),
                            ft.VerticalDivider(width=3, thickness=3, color="white"),
                            ft.Container(
                                ft.Text(List_data_for_export[3],
                                    color=ft.colors.PRIMARY,    
                                        ),
                                bgcolor=ft.colors.SECONDARY_CONTAINER,
                                alignment=ft.alignment.center,
                                width=150,
                                expand=True,
                            ),
                            ft.VerticalDivider(width=3, thickness=3, color="white"),
                            ft.Container(
                                ft.Text(List_data_for_export[4],
                                    color=ft.colors.PRIMARY,    
                                        ),
                                bgcolor=ft.colors.SECONDARY_CONTAINER,
                                alignment=ft.alignment.center,
                                width=150,
                                expand=True,
                            ),
                            ft.VerticalDivider(width=3, thickness=3, color="white"),
                            ft.Container(
                                ft.Text(List_data_for_export[5],
                                    color=ft.colors.PRIMARY,    
                                        ),
                                bgcolor=ft.colors.PRIMARY_CONTAINER,
                                alignment=ft.alignment.center,
                                width=150,
                                #expand=True,
                            ),
                            ft.VerticalDivider(width=3, thickness=3, color="white"),
                            ft.Container(
                                ft.Text(List_data_for_export[6],
                                    color=ft.colors.PRIMARY,    
                                        ),
                                bgcolor=ft.colors.PRIMARY_CONTAINER,
                                alignment=ft.alignment.center,
                                width=150,
                                #expand=True,
                            ),
                        ],
                    ),
                ],
                ),
                )
                df = pd.concat([df, pd.DataFrame([List_data_for_export], columns=list(['Data', 'Concurso', 'Numeros Sorteados', 'Ganhadores', 'Apostas ganhadoras', 'Arrecadação', 'Acumulou?']))], ignore_index=True)
                df.to_excel(save_sheet, index=False)

        if df['Concurso'].isna().all():
            concurso_input = ft.Text()
            input_c = ft.TextField(label="Concurso", hint_text="Por favor digite o número do concurso")
            get_concurso_data = ft.ElevatedButton(text="Confirmar", on_click=concurso_get)
            page.add(input_c, get_concurso_data, concurso_input)

        else:    
            ultimo_concurso_salvo = str(df['Concurso'].iloc[-1])   

            #A classe Service é utilizada para criar uma instância do Chrome WebDriver 
            service = Service()

            #webdriver.ChromeOptions é utilizado para definir a preferência para o browser do Chrome
            options = webdriver.ChromeOptions()
            #options.add_argument("--headless=new")

            #Inicia-se a instância do Chrome WebDrive com as classes definidas, service e options 
            driver = webdriver.Chrome(service = service, options = options)

            #URL de onde vamos pegar os dados
            url = 'https://loterias.caixa.gov.br/Paginas/Lotofacil.aspx'
            #headers = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"}

            #Acessando a URL
            driver.get(url)
            time.sleep(2)

            #como encontrar elementos do HTML
            #find_element(By.ID, "id")
            #find_element(By.NAME, "name")
            #find_element(By.XPATH, "xpath")
            #find_element(By.LINK_TEXT, "link text")
            #find_element(By.PARTIAL_LINK_TEXT, "partial link text")
            #find_element(By.TAG_NAME, "tag name")
            #find_element(By.CLASS_NAME, "class name")
            #find_element(By.CSS_SELECTOR, "css selector")

            #buscar textos no HTML
            #td.get_attribute('innerHTML')
            #td.get_attribute('innerText')
            #td.get_attribute('textContent')
            
            #Captura dos dados

            #Capturando a data
            lotofacil_data = driver.find_elements(By.XPATH, "//*[@id='wp_resultados']/div[1]/div/h2/span")[0].text
            #separando a string que contém concurso e data
            Concurso,Data = lotofacil_data.split('(', 1)
            Concurso = Concurso.replace('Concurso ', '')
            #removendo o parenteses da data
            #Data = Data.replace(')', '')
            #Data = datetime.datetime.strptime(Data, '%d/%m/%Y')
            
            #ultimo_concurso_salvo = str(df['Concurso'].iloc[-1])
            ultimo_concurso_salvo = ultimo_concurso_salvo.replace('Concurso ', '')

            #ultima_data_exc = df['Data'].iloc[-1]
            #ultima_data_exc_tratada = datetime.datetime.strptime(ultima_data_exc, '%d/%m/%Y')
            #data_atual = format(datetime.datetime.now(), '%d/%m/%Y')
            #data_atual_tratada = datetime.datetime.strptime(data_atual, '%d/%m/%Y')
            #data_atual_tratada = data_atual_tratada - datetime.timedelta(days=1)
            #diferenca = data_atual_tratada - ultima_data_exc_tratada
            #difference_list = []

            old_concurso = driver.find_element(By.XPATH, "//*[@id='buscaConcurso']").click()

            print(Concurso)
            print(ultimo_concurso_salvo)

            #Se o último concurso salvo na planilha não for igual ao atual no site o sistema voltará e capturará todos os ainda não
            #capturados até o mais atual
            for i in range(int(ultimo_concurso_salvo)+1,int(Concurso)+1):
                
                driver.find_element(By.XPATH, "//*[@id='buscaConcurso']").click
                time.sleep(2)
                driver.find_element(By.XPATH, "//*[@id='buscaConcurso']").send_keys(i)
                time.sleep(2)
                pyautogui.press('ENTER') 
                time.sleep(2)
                pyautogui.press('backspace')
                pyautogui.press('backspace')
                pyautogui.press('backspace')
                pyautogui.press('backspace')
                time.sleep(2)
                #Capturando a data
                lotofacil_data = driver.find_elements(By.XPATH, "//*[@id='wp_resultados']/div[1]/div/h2/span")[0].text
                #Capturando os números sorteados
                lotofacil_numbers = driver.find_elements(By.CSS_SELECTOR, ".ng-binding.dezena.ng-scope")[0:15]
                #Capturando o texto dos números para cada número na lista
                all_lotofacil_numbers = [number.get_attribute('innerText') for number in lotofacil_numbers]
                #Capturando os ganhadores
                lotofacil_ganhadores = driver.find_elements(By.CSS_SELECTOR, ".description.ng-binding.ng-scope")[0:5]
                #Capturando o texto dos números para cada ganhador na lista
                all_lotofacil_winners = [winner.get_attribute('innerText') for winner in lotofacil_ganhadores]
                #Capturando a arrecadação total
                lotofacil_dados_extras = driver.find_elements(By.XPATH, "//div[contains(@class, 'related-box gray-text no-margin')]/p")[6:27]
                #Capturando o texto da arrecadação
                lotofacil_dados_extras_text = [arrecadacao_details.get_attribute('innerText') for arrecadacao_details in lotofacil_dados_extras]


                #Tratamento dos dados
                #separando a string que contém concurso e data
                Concurso,Data = lotofacil_data.split('(', 1)
                #tirando ')' da data
                Data = Data.replace(')','')
                #Transformando o array de números sorteados em string separados por '-'
                loteria_numbers_to_string = ' - '.join(str(x) for x in all_lotofacil_numbers)
                #Transformando o array de ganhadores em string separados por '-'
                loteria_winners_to_string = ' - '.join(str(x) for x in all_lotofacil_winners)
                #Transformando o array que traz a arrecadação e dados extras em string separada por ' '
                lotofacil_dados_extras_text_tratado = ''.join(str(x) for x in lotofacil_dados_extras_text)
                #remove os textos a mais deixando apenas o valor da arrecadação e separa dos dados extras
                detalhamento,arrecadacao = lotofacil_dados_extras_text_tratado.split('R$', 1)
                arrecadacao = arrecadacao.replace(' Veja o detalhamento', '')
                #Saber se houve ganhador ou acumulou
                if 'Não houve acertador' in loteria_winners_to_string: 
                    loteria_acumulou = 'Acumulou!'
                else:
                    loteria_acumulou = 'Houve Ganhador'

                #Transformando todos os dados coletados em um array
                List_data_for_export = [Data,Concurso,loteria_numbers_to_string,loteria_winners_to_string,detalhamento,arrecadacao,loteria_acumulou]

                #print(ultima_data_exc_tratada)
                #print(data_atual_tratada)
                #print(diferenca)
                #print(Data)
                #print(Concurso)
                #print(loteria_numbers_to_string)
                #print(loteria_winners_to_string)
                #print(detalhamento)
                #print(arrecadacao)
                #print(loteria_acumulou)
                #print(List_data_for_export)

                page.add(
                    ft.Column(
                    scroll=ft.ScrollMode.ALWAYS,
                    controls=[
                        ft.Row(
                            spacing=0,
                            alignment=ft.alignment.center,
                            height=350,
                            controls=[
                            ft.Container(
                                ft.Text(List_data_for_export[0],
                                    color=ft.colors.PRIMARY,    
                                        ),
                                bgcolor=ft.colors.SECONDARY_CONTAINER,
                                alignment=ft.alignment.center,
                                width=150,
                                #expand=True,
                            ),
                            ft.VerticalDivider(width=3, thickness=3, color="white"),
                            ft.Container(
                                ft.Text(List_data_for_export[1],
                                    color=ft.colors.PRIMARY,    
                                        ),
                                bgcolor=ft.colors.PRIMARY_CONTAINER,
                                alignment=ft.alignment.center,
                                width=150,
                                #expand=True,
                            ),
                            ft.VerticalDivider(width=3, thickness=3, color="white"),
                            ft.Container(
                                ft.Text(List_data_for_export[2],
                                    color=ft.colors.PRIMARY,    
                                        ),
                                bgcolor=ft.colors.PRIMARY_CONTAINER,
                                alignment=ft.alignment.center,
                                width=150,
                                #expand=True,
                            ),
                            ft.VerticalDivider(width=3, thickness=3, color="white"),
                            ft.Container(
                                ft.Text(List_data_for_export[3],
                                    color=ft.colors.PRIMARY,    
                                        ),
                                bgcolor=ft.colors.SECONDARY_CONTAINER,
                                alignment=ft.alignment.center,
                                width=150,
                                expand=True,
                            ),
                            ft.VerticalDivider(width=3, thickness=3, color="white"),
                            ft.Container(
                                ft.Text(List_data_for_export[4],
                                    color=ft.colors.PRIMARY,    
                                        ),
                                bgcolor=ft.colors.SECONDARY_CONTAINER,
                                alignment=ft.alignment.center,
                                width=150,
                                expand=True,
                            ),
                            ft.VerticalDivider(width=3, thickness=3, color="white"),
                            ft.Container(
                                ft.Text(List_data_for_export[5],
                                    color=ft.colors.PRIMARY,    
                                        ),
                                bgcolor=ft.colors.PRIMARY_CONTAINER,
                                alignment=ft.alignment.center,
                                width=150,
                                #expand=True,
                            ),
                            ft.VerticalDivider(width=3, thickness=3, color="white"),
                            ft.Container(
                                ft.Text(List_data_for_export[6],
                                    color=ft.colors.PRIMARY,    
                                        ),
                                bgcolor=ft.colors.PRIMARY_CONTAINER,
                                alignment=ft.alignment.center,
                                width=150,
                                #expand=True,
                            ),
                        ],
                    ),
                ],
                ),
                )
                df = pd.concat([df, pd.DataFrame([List_data_for_export], columns=list(['Data', 'Concurso', 'Numeros Sorteados', 'Ganhadores', 'Apostas ganhadoras', 'Arrecadação', 'Acumulou?']))], ignore_index=True)
                df.to_excel(save_sheet, index=False)    

    def call_save_sheet(e):
        page.controls.clear()
        page.add(
        ft.Row(
        [
        ft.Container(
            ft.ElevatedButton(
                "Carregar planilha salva",
                icon=ft.icons.FILE_UPLOAD_OUTLINED,
                on_click=lambda _: save_file_dialog.pick_files(
                ),
            ),
        bgcolor=ft.colors.PRIMARY,
        alignment=ft.alignment.center_left,
        padding=5,
        height=100, 
        ),
        ],
        spacing=5,
        ),
        )

    def call_new_sheet(e):
        page.controls.clear()
        page.add(
        ft.Row(
        [
        ft.Container(
            ft.ElevatedButton(
                "Criar um novo arquivo",
                icon=ft.icons.FILE_UPLOAD_OUTLINED,
                on_click=new_sheet(
                ),
            ),
        bgcolor=ft.colors.PRIMARY,
        alignment=ft.alignment.center_left,
        padding=5,
        height=100, 
        ),
        ],
        spacing=5,
        ),
        )
        
    #criar uma planilha nova com as colunas padronizadas
    def new_sheet():

        df = pd.DataFrame(columns=['Data', 'Concurso', 'Numeros Sorteados', 'Ganhadores', 'Apostas ganhadoras', 'Arrecadação', 'Acumulou?'])

        #df = df.set_axis(['Data', 'Concurso', 'Numeros Sorteados', 'Ganhadores', 'Detalhamento sobre apostas ganhadoras', 'Arrecadação', 'Acumulou ou houve ganhador?'], axis=1)

        df.to_excel("Catalogo_Plataforma_Essenciz_IS8_tratado.xlsx", index=False)

    def sheet_values_datatable(e: FilePickerResultEvent):
        save_file_dir_datable = ft.Text()
        save_file_dir_datable.value = (
        ", \n".join(map(lambda f: f.path, e.files)) if e.files else "Ao menos um arquivo é obrigatório"
        )
        print(save_file_dir_datable) 
 
        save_file_dir_datatable1 = str(save_file_dir_datable).replace("text {'value': '", '')
        save_file_dir_datatable2 = str(save_file_dir_datatable1).replace("'}", '')
        print(save_file_dir_datatable2)

        global save_sheet_datatable 
        save_sheet_datatable = save_file_dir_datatable2   

    save_file_dialog_datatable = FilePicker(on_result=sheet_values_datatable)
     
    page.overlay.append(save_file_dialog_datatable)

    #Defina o que é carregado em cada aba do menu inferior
    def data_base(e):
        if e.control.selected_index == 0:
            page.controls.clear()
            page.add(
                ft.Row(
                    [
                ft.Container(
                calling_load_sheet(
                    "Já possui um arquivo?",
                    icon=ft.icons.UPLOAD_FILE,
                    on_click=call_save_sheet,
                ),
                bgcolor=ft.colors.PRIMARY,
                alignment=ft.alignment.center,
                padding=5,
                height=100,
                expand=True,
                ),  

                ft.Divider(height=9, thickness=3),

                ft.Container(
                ft.ElevatedButton(
                    "Criar um novo arquivo",
                    icon=ft.icons.FIBER_NEW_OUTLINED,
                    on_click=call_new_sheet,
                ),
                bgcolor=ft.colors.PRIMARY,
                alignment=ft.alignment.center,
                padding=5,
                height=100,
                expand=True,
                ),  
            ],
            spacing=10,
            ),
            )
            page.update()
        
        if e.control.selected_index == 1:
            page.controls.clear()
            df = pd.read_excel(save_sheet)
            json_str = df.to_json()
            df_table = pd.read_json(json_str)

            all_data_table = df_table.to_dict(orient="records")

            def get_concurso(e):
                datatable.rows.clear()
                global conc_filtered
                conc_filtered = "Concurso " + search_filter.value
                print(conc_filtered)

                list_to_show = [i for i in all_data_table if conc_filtered in i['Concurso']]

                for i in list_to_show:
                    datatable.rows.append(
                        DataRow(
                            cells=[
                                DataCell(Text(i['Data'])),
                                DataCell(Text(i['Concurso'])),
                                DataCell(Text(i['Numeros Sorteados'])),
                                DataCell(Text(i['Ganhadores'])),
                                DataCell(Text(i['Apostas ganhadoras'])),
                                DataCell(Text(i['Arrecadação'])),
                                DataCell(Text(i['Acumulou?'])),
                            ],
                        ),
                    )
                page.update(datatable)

            ultimas_datas = df['Data']
            ultimas_datas = ultimas_datas.to_string(index=False)
            ultimas_datas = ultimas_datas.split('\n')
            df_ult_ano = []

            #print(ultimas_datas)

            for i in ultimas_datas:
                df_ult_ano.append(i[6:10])
            df_ult_ano = list(set(df_ult_ano))     
            print(df_ult_ano)    

            def dropdown_changed_year(e):
                global drop_selected_year
                drop_selected_year = drop_data_year.value
                print(drop_selected_year)

                df_ult_mes = []

                for i in ultimas_datas:
                    if i[6:10] == drop_selected_year:
                        df_ult_mes.append(i[3:5])
                        df_ult_mes = list(set(df_ult_mes))     
                print(df_ult_mes)

                drop_data.options.clear()
                for i in df_ult_mes:
                    drop_data.options.append(
                    ft.dropdown.Option(i),
                )
                page.update()

            def dropdown_changed_month(e):
                datatable.rows.clear()
                #t.value = f"Dropdown value is:  {drop_data.value}"

                drop_selected = drop_data.value
                print(drop_data.value)

                df_tb_conc_values = df[['Data']]
                df_tb_conc_values = df_tb_conc_values.to_string(index=False, header=None)
                #df_dt_arrecada_values = df_dt_arrecada_values.replace('\n','  ').split('  ')
                df_tb_conc_values = df_tb_conc_values.split('\n')
                #print(df_dt_arrecada_values)
                df_data_filtered = []
                for i in df_tb_conc_values:
                    if i[3:5] == drop_selected and i[6:10] == drop_selected_year:
                        df_data_filtered.append(i[:10])

                print(df_data_filtered)  

                for i in all_data_table:
                    for x in df_data_filtered:
                        if i['Data'] == x:
                            datatable.rows.append(
                                DataRow(
                                    cells=[
                                        DataCell(Text(i['Data'])),
                                        DataCell(Text(i['Concurso'])),
                                        DataCell(Text(i['Numeros Sorteados'])),
                                        DataCell(Text(i['Ganhadores'])),
                                        DataCell(Text(i['Apostas ganhadoras'])),
                                        DataCell(Text(i['Arrecadação'])),
                                        DataCell(Text(i['Acumulou?'])),
                                    ],
                                ),
                            )
                    page.update(datatable)  

            drop_data = ft.Dropdown(
                label="Mês",
                #width=200,
                on_change=dropdown_changed_month,
                options=[],
                expand=True
            )
            

            drop_data_year = ft.Dropdown(
                label="Ano",
                #width=200,
                on_change=dropdown_changed_year,
                options=[],
                expand=True
            )
            

            for i in df_ult_ano:
                drop_data_year.options.append(
                    ft.dropdown.Option(i),
                )
            page.update()     

            search_filter = ft.CupertinoTextField(
                placeholder_text="Digite apenas o número do concurso",
                input_filter=ft.InputFilter(allow=True, regex_string=r"^[0-9]*$", replacement_string=""),
                height=60,
                expand=True
            )
            page.add(
                Column([
                    Text("Base de Resultados Capturados", size=30, weight="bold"),
                    ft.Row([drop_data_year, drop_data]),
                    ft.Row([search_filter,
                    ft.ElevatedButton(text="Filtrar", on_click=get_concurso)
                    ])
                ])
            )  

            global datatable

            datatable = DataTable(
            border_radius=10,
            border=ft.border.all(2, ft.colors.PRIMARY),
            data_row_max_height=float("inf"),
            heading_row_color=ft.colors.SECONDARY_CONTAINER,
            columns=[
                DataColumn(Text("Data",color=ft.colors.PRIMARY,)),
                DataColumn(Text("Concurso",color=ft.colors.PRIMARY,)),
                DataColumn(Text("Numeros Sorteados",color=ft.colors.PRIMARY)),
                DataColumn(Text("Ganhadores",color=ft.colors.PRIMARY,)),
                DataColumn(Text("Apostas ganhadoras",color=ft.colors.PRIMARY,)),
                DataColumn(Text("Arrecadação",color=ft.colors.PRIMARY,)),
                DataColumn(Text("Acumulou?",color=ft.colors.PRIMARY,)),
            ],
            rows=[],
            )
        
            for i in all_data_table:
                datatable.rows.append(
                    DataRow(
                        cells=[
                            DataCell(Text(i['Data'])),
                            DataCell(Text(i['Concurso'])),
                            DataCell(Text(i['Numeros Sorteados'])),
                            DataCell(Text(i['Ganhadores'])),
                            DataCell(Text(i['Apostas ganhadoras'])),
                            DataCell(Text(i['Arrecadação'])),
                            DataCell(Text(i['Acumulou?'])),
                        ],
                    ),
                )
            page.add(datatable)

        if e.control.selected_index == 2:
            page.controls.clear()
            df = pd.read_excel(save_sheet)
            df_num_rep = df['Numeros Sorteados']
            pd.options.display.max_colwidth = 1000
            df_num_rep = df_num_rep.to_string(index=False)
            df_num_rep = df_num_rep.replace('\n',' - ').split(' - ')
            df_num_rept = {i:df_num_rep.count(i) for i in df_num_rep}
            #print(df_num_rep)
            #print(df_num_rept)
            #print(list(df_num_rept.keys())[0])

            z_num = df['Numeros Sorteados']
            
            z_num = z_num.index.tolist()
            #print(z_num)

            locale.setlocale(locale.LC_ALL, 'pt_pt.UTF-8')

            #pegar última data Salva
            #ultima_data_salva = df['Data'].dt.strftime('%d/%m/%Y').iloc[-1]

            #ultimas_datas = df['Data'].dt.strftime('%d/%m/%Y')
            #ultimas_datas = ultimas_datas.to_string(index=False)
            #ultimos_meses = ultimas_datas.replace(' 00:00:00', '')
            #ultimos_meses = ultimos_meses.split('\n')

            ultimas_datas = df['Data']
            ultimas_datas = ultimas_datas.to_string(index=False)
            ultimas_datas = ultimas_datas.split('\n')
            df_ult_ano = []

            #print(ultimas_datas)

            for i in ultimas_datas:
                df_ult_ano.append(i[6:10])
            df_ult_ano = list(set(df_ult_ano))     
            print(df_ult_ano)
 
            #df_data_rep = df_data_rep[-30:]
            #df_data_rept = df_data_rept
            #print(len(df_data_rept))

            def dropdown_changed_year(e):
                global drop_selected_year
                drop_selected_year = drop_data_year.value
                print(drop_selected_year)

                df_ult_mes = []

                for i in ultimas_datas:
                    if i[6:10] == drop_selected_year:
                        df_ult_mes.append(i[3:5])
                        df_ult_mes = list(set(df_ult_mes))     
                print(df_ult_mes)

                drop_data.options.clear()
                for i in df_ult_mes:
                    drop_data.options.append(
                    ft.dropdown.Option(i),
                )
                page.update()

            def dropdown_changed(e):
                chart2.bar_groups.clear()
                chart2.bottom_axis.labels.clear()
                #t.value = f"Dropdown value is:  {drop_data.value}"

                drop_selected = drop_data.value
                print(drop_data.value)

                df_dt_arrecada_values = df[['Data', 'Arrecadação']]
                df_dt_arrecada_values = df_dt_arrecada_values.to_string(index=False, header=None)
                #df_dt_arrecada_values = df_dt_arrecada_values.replace('\n','  ').split('  ')
                df_dt_arrecada_values = df_dt_arrecada_values.split('\n')
                #print(df_dt_arrecada_values)
                df_data_filtered = []
                df_arrecada_values = []
                for i in df_dt_arrecada_values:
                    if i[3:5] == drop_selected and i[6:10] == drop_selected_year:
                        df_data_filtered.append(i[:10])
                        df_arrecada_values.append(i[12:26])

                print(df_arrecada_values) 
                print(df_data_filtered)

                #df_data_filtered_format = []
                #for i in df_data_filtered:
                #    df_data_filtered_format.append(datetime.datetime.strptime(i, '%Y-%m-%d').strftime('%d/%m/%Y'))

                df_dt_day_label = []
                for i in df_data_filtered:
                        df_dt_day_label.append(i[:2])       

                #print(df_arrecada_values)
                df_arrecada_values_bar = str(df_arrecada_values).replace(',00','')
                df_arrecada_values_bar = df_arrecada_values_bar.replace('.','')
                df_arrecada_values_bar = df_arrecada_values_bar.replace("',",'')
                df_arrecada_values_bar = df_arrecada_values_bar.replace("'",'')
                df_arrecada_values_bar = df_arrecada_values_bar.replace('[','')
                df_arrecada_values_bar = df_arrecada_values_bar.replace(']','')
                df_arrecada_values_bar = df_arrecada_values_bar.split()
                cash = "R$"
                brazilian_cash = [cash + i for i in df_arrecada_values]

                print(df_arrecada_values_bar)
                print(brazilian_cash)

                #valor arrecadado por data
                df_cash_rep_bar_join = dict(zip(df_dt_day_label[::1], df_arrecada_values_bar[::1]))  
            
                #labels do gráfico de arrecadação por data
                for i in df_dt_day_label:  
                    chart2.bottom_axis.labels.append(
                        ft.ChartAxisLabel(
                            value=i, label=ft.Container(ft.Text(i + '/' + drop_selected, size=10))
                        ),
                    ),
                page.update()
                       
                color_bar_data = [ft.colors.RED_300, ft.colors.GREEN_300, ft.colors.PURPLE_300, ft.colors.BLUE_300, ft.colors.AMBER_300,
                            ft.colors.BLUE_ACCENT_400, ft.colors.BLUE_GREY_300, ft.colors.AMBER_ACCENT_400, ft.colors.BROWN_300,
                            ft.colors.DEEP_ORANGE_300, ft.colors.CYAN_300, ft.colors.DEEP_PURPLE_300, ft.colors.GREEN_ACCENT_400,
                            ft.colors.PINK_ACCENT_400, ft.colors.INDIGO_300, ft.colors.INDIGO_ACCENT_400, ft.colors.LIME_300,
                            ft.colors.LIME_ACCENT_400, ft.colors.RED_ACCENT_400, ft.colors.YELLOW_ACCENT_700, ft.colors.YELLOW_700,
                            ft.colors.TEAL_ACCENT_400, ft.colors.TEAL_400, ft.colors.RED_700, ft.colors.BLUE_700, ft.colors.AMBER_900,
                            ft.colors.BLUE_900, ft.colors.BLUE_GREY_900, ft.colors.BROWN_900, ft.colors.CYAN_900]
                
                c = -1
                for data_index, cash_bar in df_cash_rep_bar_join.items():
                    c += 1
                    chart2.bar_groups.append(
                        ft.BarChartGroup(
                        x=data_index,
                        bar_rods=[
                            ft.BarChartRod(
                                from_y=0,
                                to_y=cash_bar,
                                width=30,
                                #color=color_bar[c],
                                color=color_bar_data[c],
                                tooltip=brazilian_cash[c],
                                border_radius=0,
                            ),
                        ],
                        ),
                    ),

                page.update()


            #t = ft.Text(
            #        color=ft.colors.PRIMARY,
            #        text_align=ft.TextAlign.CENTER,    
            #            )

            page.add(
            ft.Column(
                scroll=ft.ScrollMode.AUTO,
                controls=[
                ft.Row(
                [
                ft.Container( 
                ),
                ],
                height=50,
                spacing=5,
                ),
                ft.Row(
                [
                ft.Container(    
                ft.Text('NÚMEROS MAIS SORTEADOS',
                    color=ft.colors.SECONDARY_CONTAINER,
                    text_align=ft.TextAlign.CENTER,    
                        ),
                bgcolor=ft.colors.PRIMARY,
                alignment=ft.alignment.center,
                padding=5,
                height=60,
                expand=True,
                ),
                ],
                height=100,
                spacing=5,
                ),
                ],
            ),
            )

            chart = ft.BarChart(
                bar_groups=[
                    ft.BarChartGroup(),
                ],
                border=ft.border.all(1, ft.colors.PRIMARY_CONTAINER),
                left_axis=ft.ChartAxis(
                labels_size=40, title=ft.Text("Vezes que foram sorteados"), title_size=40
                ),
                bottom_axis=ft.ChartAxis(
                title=ft.Text("Números Sorteados"), title_size=40,
                labels=[
                    ft.ChartAxisLabel(
                        value=0, label=ft.Container()
                        ),
                    ],
                labels_size=40,
                ),
                horizontal_grid_lines=ft.ChartGridLines(
                color=ft.colors.PRIMARY_CONTAINER, width=1, dash_pattern=[5, 10]
                ),
                tooltip_bgcolor=ft.colors.with_opacity(0.8, ft.colors.BLACK),
                #max_y=50,
                interactive=True,
                #expand=True,
                )
            page.add(chart) 

            for i in z_num:
                chart.bottom_axis.labels.append(
                    ft.ChartAxisLabel(
                        value=i, label=ft.Container(ft.Text(i))
                    ),
                ),
            page.update()
            #(number, repeat_num), *rest = df_num_rept.items() 
             
            color_bar_num = [ft.colors.RED_300, ft.colors.GREEN_300, ft.colors.PURPLE_300, ft.colors.BLUE_300, ft.colors.AMBER_300,
                        ft.colors.BLUE_ACCENT_400, ft.colors.BLUE_GREY_300, ft.colors.AMBER_ACCENT_400, ft.colors.BROWN_300,
                        ft.colors.DEEP_ORANGE_300, ft.colors.CYAN_300, ft.colors.DEEP_PURPLE_300, ft.colors.GREEN_ACCENT_400,
                        ft.colors.PINK_ACCENT_400, ft.colors.INDIGO_300, ft.colors.INDIGO_ACCENT_400, ft.colors.LIME_300,
                        ft.colors.LIME_ACCENT_400, ft.colors.RED_ACCENT_400, ft.colors.YELLOW_ACCENT_700, ft.colors.YELLOW_700,
                        ft.colors.TEAL_ACCENT_400, ft.colors.TEAL_400, ft.colors.RED_700, ft.colors.BLUE_GREY_700]
            
            c = -1
            for key, value in df_num_rept.items():
                c += 1
                chart.bar_groups.append(
                    ft.BarChartGroup(
                    x=key,
                    bar_rods=[
                        ft.BarChartRod(
                            from_y=0,
                            to_y=value,
                            width=40,
                            color=color_bar_num[c],
                            tooltip=value,
                            border_radius=0,
                        ),
                    ],
                    ),
                ),

            page.update()

            page.add(
            ft.Column(
                scroll=ft.ScrollMode.AUTO,
                controls=[
                ft.Row(
                [
                ft.Container(
                ft.Text('ARRECADAÇÕES POR DATA',
                    color=ft.colors.SECONDARY_CONTAINER,
                    text_align=ft.TextAlign.CENTER,    
                        ),
                bgcolor=ft.colors.PRIMARY,
                alignment=ft.alignment.center,
                padding=5,
                height=60,
                expand=True,
                ),
                ],
                height=100,
                spacing=5,
                ),
                ],
            ),
            )
            
            drop_data = ft.Dropdown(
                label="Mês",
                width=200,
                on_change=dropdown_changed,
                options=[]
            )
            

            drop_data_year = ft.Dropdown(
                label="Ano",
                width=200,
                on_change=dropdown_changed_year,
                options=[]
            )
            

            for i in df_ult_ano:
                drop_data_year.options.append(
                    ft.dropdown.Option(i),
                )
            page.update()

            page.add(
            ft.Row([drop_data_year, drop_data])
            )

            chart2 = ft.BarChart(
                bar_groups=[
                    ft.BarChartGroup(),
                ],
                border=ft.border.all(1, ft.colors.PRIMARY_CONTAINER),
                left_axis=ft.ChartAxis(
                labels_size=40, title=ft.Text("Valores arrecadados"), title_size=40
                ),
                bottom_axis=ft.ChartAxis(
                title=ft.Text("Data"), title_size=40,
                labels=[
                    ft.ChartAxisLabel(
                        value=0, label=ft.Container()
                        ),
                    ],
                labels_size=40,
                ),
                horizontal_grid_lines=ft.ChartGridLines(
                color=ft.colors.PRIMARY_CONTAINER, width=1, dash_pattern=[1, 5]
                ),
                tooltip_bgcolor=ft.colors.with_opacity(0.8, ft.colors.BLACK),
                max_y=50000000,
                interactive=True,
                #expand=True,
                )
            page.add(chart2) 

        #Insights
        if e.control.selected_index == 3:
            #limpar página
            page.controls.clear()
            #ler arquivo excel
            df = pd.read_excel(save_sheet)
            #pegar dados da coluna - coluna de números sorteados
            df_num_rep = df['Numeros Sorteados']
            #definir limitação para quantidade de letras do texto capturado
            pd.options.display.max_colwidth = 1000
            df_num_rep = df_num_rep.to_string(index=False)
            df_num_rep = df_num_rep.replace('\n',' - ').split(' - ')
            df_num_rept = {i:df_num_rep.count(i) for i in df_num_rep}
            print(df_num_rep)
            print(df_num_rept)
            print(df_num_rept.values())
            maxVals = sorted(df_num_rept.values())[-10:]
            print(maxVals)
            maxVals2 = dict(Counter(df_num_rept).most_common(5))
            print(maxVals2)

            #pegar dados da coluna - coluna de Apostas ganhadoras
            df_betwin_rep = df['Apostas ganhadoras']
            df_betwin_rep = df_betwin_rep.to_string(index=False)

            df_betwin_rep = df_betwin_rep.replace('\\n', ' - ')
            df_betwin_rep = df_betwin_rep.replace(' o prêmio para 15 acertos', '\n')
            df_betwin_rep = df_betwin_rep.replace('NaN', '')
            df_betwin_rep = df_betwin_rep.split(' - ')
            df_betwin_rep = [word for word in df_betwin_rep if len(word) <= 2]
            df_betwin_rept = dict(Counter(df_betwin_rep).most_common(5))
            print(df_betwin_rep)
            print(df_betwin_rept)

            #pegar dados da coluna - coluna de Ganhadores
            df_winners_rep = df['Ganhadores']
            df_winners_rep = df_winners_rep.to_string(index=False)
            df_winners_rep = df_winners_rep.replace('\\n', ' - ')
            df_winners_rep = df_winners_rep.replace('\n    ', ' - ')
            df_winners_rep = df_winners_rep.split(' - ')
            df_winners_rept = dict(Counter(df_winners_rep).most_common(5))
            print(df_winners_rep)
            print(df_winners_rept)

            #pegar dados da coluna - coluna Acumulou?
            df_win_rep = df['Acumulou?'].value_counts()
            print(df_win_rep)

            #numeros
            def items_num(count):
                items_num = []
                for key, value in maxVals2.items():
                    items_num.append(
                        ft.Container(
                            content=ft.Text(('O número ' + key + ' se repetiu ' + str(value) + ' vezes no período')),
                            alignment=ft.alignment.center,
                            height=50,
                            bgcolor=ft.colors.PRIMARY_CONTAINER,
                        )
                    )
                return items_num
            
            #acumulou?
            def items_win(count):
                items_win = []
                for win, count in df_win_rep.items():
                    items_win.append(
                        ft.Container(
                            content=ft.Text((str(win) + ' ' + str(count) + ' vezes')),
                            alignment=ft.alignment.center,
                            height=140,
                            bgcolor=ft.colors.PRIMARY_CONTAINER,
                        )
                    )
                return items_win
            
            #ganhadores por uf
            def items_uf(count):
                items_uf = []
                for uf, count in df_betwin_rept.items():
                    items_uf.append(
                        ft.Container(
                            content=ft.Text((uf + ' teve ganhadores ' + str(count) + ' vezes')),
                            alignment=ft.alignment.center,
                            height=50,
                            bgcolor=ft.colors.PRIMARY_CONTAINER,
                        )
                    )
                return items_uf
            
            #Qtd de números acertados
            def items_winners(count):
                items_winners = []
                for winner, count in df_winners_rept.items():
                    items_winners.append(
                        ft.Container(
                            content=ft.Text((winner + ' ocorreram ' + str(count) + ' vezes')),
                            alignment=ft.alignment.center,
                            height=50,
                            bgcolor=ft.colors.PRIMARY_CONTAINER,
                        )
                    )
                return items_winners

            def column_with_alignment(align: ft.MainAxisAlignment):
                return ft.Column(
                        scroll=ft.ScrollMode.AUTO,
                        controls=[
                            #Titulo dos insights
                            ft.Row(
                            spacing=0,
                            alignment=ft.alignment.center,
                            height=50,
                            controls = [
                                ft.Container(
                                ft.Text(str('TOP 5 NÚMEROS MAIS SORTEADOS'), size=15),
                                alignment=ft.alignment.center,
                                height=100,
                                bgcolor=ft.colors.PRIMARY_CONTAINER,
                                expand=True,
                                ),

                                #linha divisória vertical    
                                ft.VerticalDivider(width=4, thickness=3, color=ft.colors.with_opacity(0.05, ft.colors.PRIMARY)),

                                ft.Container(
                                ft.Text(str('TOP 5 GANHADORES POR UF'), size=15),
                                alignment=ft.alignment.center,
                                height=100,
                                bgcolor=ft.colors.PRIMARY_CONTAINER,
                                expand=True,
                                ),
                            ],
                            ),
                            #resultados dos insights
                            ft.Row(
                            spacing=0,
                            alignment=ft.alignment.center,
                            #height=50,
                            controls = [
                                ft.Container(
                                    content=ft.Column(items_num(5), alignment=align),
                                    bgcolor=ft.colors.SECONDARY,
                                    expand=True,
                                ),

                                #linha divisória vertical
                                ft.VerticalDivider(width=5, thickness=3),

                                ft.Container(
                                    content=ft.Column(items_uf(5), alignment=align),
                                    bgcolor=ft.colors.SECONDARY,
                                    expand=True,
                                ),
                            ],
                            ),
                            ft.Row(
                            spacing=0,
                            alignment=ft.alignment.center,
                            height=50,
                            controls = [
                                ft.Container(
                                ft.Text(str('VEZES EM QUE HOUVERAM GANHADORES'), size=15),
                                alignment=ft.alignment.center,
                                height=100,
                                bgcolor=ft.colors.PRIMARY_CONTAINER,
                                expand=True,
                                ),

                                #linha divisória vertical    
                                ft.VerticalDivider(width=4, thickness=3, color=ft.colors.with_opacity(0.05, ft.colors.PRIMARY)),

                                ft.Container(
                                ft.Text(str('QUANTIDADE DE ACERTOS'), size=15),
                                alignment=ft.alignment.center,
                                height=100,
                                bgcolor=ft.colors.PRIMARY_CONTAINER,
                                expand=True,
                                ),
                            ],
                            ),
                            ft.Row(
                            spacing=0,
                            alignment=ft.alignment.center,
                            #height=50,
                            controls = [
                                ft.Container(
                                    content=ft.Column(items_win(5), alignment=align),
                                    bgcolor=ft.colors.SECONDARY,
                                    expand=True,
                                ),

                                #linha divisória vertical
                                ft.VerticalDivider(width=5, thickness=3),

                                ft.Container(
                                    content=ft.Column(items_winners(5), alignment=align),
                                    bgcolor=ft.colors.SECONDARY,
                                    expand=True,
                                ),
                            ],
                            ),
                        ],
                        expand=True,
                    )
            
            page.add(
                ft.Row(
                    [
                        column_with_alignment(ft.MainAxisAlignment.START),
                        #column_with_alignment(ft.MainAxisAlignment.CENTER),
                        #column_with_alignment(ft.MainAxisAlignment.END),
                        #column_with_alignment(ft.MainAxisAlignment.SPACE_BETWEEN),
                        #column_with_alignment(ft.MainAxisAlignment.SPACE_AROUND),
                        #column_with_alignment(ft.MainAxisAlignment.SPACE_EVENLY),
                    ],
                    spacing=10,
                    alignment=ft.MainAxisAlignment.START,
                )
            )    


    #Menu de opções inferior
    
    page.navigation_bar = ft.NavigationBar(
        on_change=data_base,
        destinations=[
            ft.NavigationBarDestination(
                icon=ft.icons.FILE_COPY_OUTLINED, 
                selected_icon=ft.icons.FILE_COPY_ROUNDED,
                label="Arquivo(Carregar/Criar)"
                ),
                ]
    )    
 
    save_file_dialog = FilePicker(on_result=sheet_values)
     
    page.overlay.append(save_file_dialog)

    calling_load_sheet = ft.ElevatedButton

    page.add(
        ft.Row(
            [
        ft.Container(
        calling_load_sheet(
            "Já possui um arquivo?",
            icon=ft.icons.UPLOAD_FILE,
            on_click=call_save_sheet,
        ),
        bgcolor=ft.colors.PRIMARY,
        alignment=ft.alignment.center,
        padding=5,
        height=100,
        expand=True,
        ),  

        ft.Divider(height=9, thickness=3),

        ft.Container(
        ft.ElevatedButton(
            "Criar um novo arquivo",
            icon=ft.icons.FIBER_NEW_OUTLINED,
            on_click=call_new_sheet,
        ),
        bgcolor=ft.colors.PRIMARY,
        alignment=ft.alignment.center,
        padding=5,
        height=100,
        expand=True,
        ),  
    ],
    spacing=10,
    ),
    )
    page.update()

ft.app(target=main)
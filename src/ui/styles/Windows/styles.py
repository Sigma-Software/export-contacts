user_form_styles = '''
    QWidget {
        font-family: Segoe UI;
    }
    QLabel {
        color: #fff;
        font-size: 15px;
    }
    QGroupBox {
        border: none;
    }
    QLineEdit {
        border: 2 solid #7a7b7b;
        height: 32px;
        font-size: 15px;
        line-height: 20px;
    }
    QCheckBox {
        color: #fff;
        font-size: 15px;
        line-height: 20px;
    }
    #logo {
        margin-bottom: 45;
    }
    #header-title {
        font-weight: 300;
        font-size: 34px;
        line-height: 40px;
        color: #e2e2e2;
    }
    #info {
        margin-bottom: 25;
    }
    #info, #exclude-info {
        font-size: 12px;
        line-height: 16px;
        color: rgba(255, 255, 255, 0.6);
    }
    #username-title, #email-title, #password-title, #exclude-title, #email_service_address-title {
        font-size: 15px;
        line-height: 20px;
    }
    #exclude-info {
        padding-bottom: 20px;
    }
    #exclude-switcher {
        border: none;
        text-align: left;
        color: #fff;
        font-size: 15px;
    }
    #export_btn {
        background-color: #cccccd;
        font-size: 15px;
        color: #000100;
    }
'''

export_btn_disabled = '''
    background-color: #cccccd;
    font-size: 15px;
    color: #000100;
'''
export_btn_enabled = '''
    background-color: #0079d8;
    font-size: 15px;
    color: #fff;
'''

exclude_domains_styles = '''
    QWidget {
        font-family: Segoe UI;
    }
    QGroupBox{
        border: none;
    }
    QScrollArea {
        background-color: transparent;
        border: none;
        margin-left: 2px;
        margin-right: 2px;
    }  
    #info-box {
        color: #fff;
    }
    #header-title {
        font-size: 46px;
        font-weight: 300;
        line-height: 56px;
        color: #fff;
    }
    #header-text {
        color: rgba(255, 255, 255, 153);
        font-size: 15px;
        line-height: 20px;
    }
    #exclude-label {
        color: #fff;
        font-size: 15px;
        line-height: 20px;
    }
    #title-input {
        border-left: 2px solid #7a7b7b;
        border-right: none;
        border-top: 2px solid #7a7b7b;
        border-bottom: 2px solid #7a7b7b;
    }
    #title-input, #title-add-btn {
        background-color: #fff;         
    }
    #title-add-btn {
        padding-right: 10px;
        border-right: 2px solid #7a7b7b;
        border-left: none;
        border-top: 2px solid #7a7b7b;
        border-bottom: 2px solid #7a7b7b;
    }
'''

domains_visible_style = '''
    #info-box {
        margin-bottom: 0;
        color: #fff;
    }
    #header-title {
        font-size: 46px;
        line-height: 56px;
        color: #fff;
    }
    #header-text {
        color: rgba(255, 255, 255, 153);
        font-size: 15px;
        line-height: 20px;
    }
    #title-add-btn, #title-input {
        background-color: #7a7a7a;
    }
'''

domains_invisible_style = '''
    #info-box {
        padding-bottom: 0;
        color: #fff;
    }
    #header-title {
        font-size: 46px;
        line-height: 56px;
        color: #fff;
    }
    #header-text {
        color: rgba(255, 255, 255, 153);
        font-size: 15px;
        line-height: 20px;
    }
'''


crisp_styles = '''
    QWidget {
        background-color: #2b2b2b;
        padding-top: 23;
        padding-bottom: 24;
        border: #fff;
    }
    #crisp-title {
        color: #fff;
        padding-right: 0;
        padding-left: 13;
        border-top-left-radius: 15px;
        border-bottom-left-radius: 15px;
    }
    #close-crisp {
        padding-left: 5;
        padding-right: 10;
        text-align: right;
        border-top-right-radius: 15px;
        border-bottom-right-radius: 15px;
    }
'''

error_popup_style = '''
    QWidget {
        font-family: Segoe UI;
    }
    #main {
        background-color: #e65c3e;
    }
    #body {
        background-color: #ffe7e0;
    }
    QLabel {
        color: #000;
    }
    #type-msg {
        font-size: 17px;
        font-weight: 600;
        line-height: 20px;
        font-weight: bold;
    }
    #message {
        font-size: 15px;
        line-height: 20px;
        margin-bottom: 15;
    }
    #close-btn {
        border: none;
        margin-left: 0;
        margin-right: 0;
        text-align: right;
    }
'''

success_popup_style = '''
    QWidget {
        font-family: Segoe UI;
    }
    #main {
        background-color: #81c785;
    }
    #body {
        background-color: #e6f4e7;
    }
    QLabel {
        color: #000;
    }
    #type-msg {
        font-size: 17px;
        font-weight: 600;
        line-height: 20px;
        font-weight: bold;
    }
    #message {
        font-size: 15px;
        line-height: 20px;
        padding-bottom: 10;
    }
    #close-btn {
        border: none;
        margin-left: 0;
        margin-right: 0;
        text-align: right;
    }
'''

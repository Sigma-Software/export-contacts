user_form_styles = '''
    QWidget {
        font-family: Helvetica Neue;
    }
    QLabel {
        color: #fff;
        font-size: 15px;
    }
    QCheckBox {
        font-size: 15px;
        line-height: 20px;
        color: rgba(255, 255, 255, 0.85);
    }
    QGroupBox {
        border: none;
    }
    QPushButton {
        border-radius: 6px;
    }
    QLineEdit {
        border: 0.5px solid rgba(255, 255, 255, 0.05);
        height: 15px;
        font-size: 13px;
        background-color: rgba(255, 255, 255, 0.05);
        color: rgba(255, 255, 255, 0.85);
    }
    #header-title {
        font-family: Helvetica Neue;
        font-weight: 300;
        font-size: 28px;
        line-height: 40px;
        color: #e2e2e2;
    }
    #info, #exclude-info {
        font-size: 11px;
        line-height: 16px;
        color: rgba(255, 255, 255, 0.6);
    }
    #username-title, #email-title, #password-title, #exclude-title, #email_service_address-title {
        font-size: 15px;
        line-height: 20px;
        color: rgba(255, 255, 255, 0.85);
    }
    #exclude-switcher {
        border: none;
        color: rgba(255, 255, 255, 0.6);
        font-size: 11px;
        line-height: 15px;
    }
'''

export_btn_disabled = '''
    background-color: #444444;
    font-size: 15px;
    color: rgba(255, 255, 255, 0.3);            
'''

export_btn_enabled = '''
    background-color: #3880d1;
    font-size: 15px;
    color: #e7ebfd;
'''

exclude_domains_styles = '''
    QWidget {
        font-family: Helvetica Neue;
    }
    QGroupBox {
        border: 1 px solid red;
    }
    QScrollArea {
        background-color: transparent;
        border: none;
        margin-left: 2px;
        margin-right: 2px;
    }
    QScrollBar:vertical {
        border: 0px solid #999999;
        background:transparent;
        width:10px;    
        margin: 0px 0px 0px 0px;
    }
    QScrollBar::handle:vertical {         
        min-height: 0px;
        border: 0px solid red;
        border-radius: 4px;
        background-color: #2b2b2b;
    }
    QScrollBar::add-line:vertical {       
        height: 0px;
        subcontrol-position: bottom;
        subcontrol-origin: margin;
    }
    QScrollBar::sub-line:vertical {
        height: 0 px;
        subcontrol-position: top;
        subcontrol-origin: margin;
    }
    #info-box {
        color: #fff;
    }
    #header-title {
        font-family: Helvetica Neue;
        font-weight: 300;
        font-size: 40px;
        line-height: 56px;
        color: rgba(255, 255, 255, 0.85);
    }
    #header-text {
        color: rgba(255, 255, 255, 0.5);
        font-size: 13px;
        line-height: 19px;
    }
    #exclude-label {
        margin-top:0;
        margin-bottom: 0;
        color: #fff;
        font-size: 13px;
    }
    #title-input {
        border-left: 2px solid #7a7b7b;
        border-right: none;
        color: rgba(255, 255, 255, 0.85);
        border-top: 2px solid #7a7b7b;
        border-bottom: 2px solid #7a7b7b;
    }
    #title-input, #title-add-btn {
        background-color: rgba(0, 0, 0, 0.1);         
    }
    #title-add-btn {
        padding-right: 5px;
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
        font-family: Helvetica Neue;
        font-weight: 300;
        font-size: 40px;
        line-height: 56px;
        color: #fff;
    }
    #header-text {
        color: rgba(255, 255, 255, 153);
        font-size: 13px;
        line-height: 19px;
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
        font-size: 40px;
        font-weight: 300;
        line-height: 56px;
        color: #fff;
    }
    #header-text {
        color: rgba(255, 255, 255, 153);
        font-size: 13px;
        line-height: 19px;
    }
'''

crisp_styles = '''
    QWidget {
        border-bottom: 1.5px solid  rgba(0, 0, 0, 0.05);
        border-top: 1.5px solid  rgba(255, 255, 255, 0.05);
        background-color: rgba(255, 255, 255, 0.05);
        padding: 23;
    }
    #crisp-title {
        color: #fff;
        padding-right: 0;
        padding-left: 15;
        font-size: 13px;
        border-left: 1px solid  rgba(0, 0, 0, 0.05);
        border-right: none;
        border-top-left-radius: 3px;
        border-bottom-left-radius: 3px;
    }
    #close-crisp {
        padding-left: 5;
        padding-right: 5;
        border-right: 1px solid  rgba(0, 0, 0, 0.05);

        border-left: none;
        border-top-right-radius: 3px;
        border-bottom-right-radius: 3px;
    }
'''

error_popup_style = '''
    QWidget {
        font-family: Helvetica Neue;
    }
    #main {
        background-color: #e65c3e;
    }
    #body {
        background-color: #ffe7e0;
    }
    QGroupBox {
        border-radius: 6px;
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

success_popup_style = '''
    QWidget {
        font-family: Helvetica Neue;
    }
    #main {
        background-color: #81c785;
    }
    #body {
        background-color: #e6f4e7;
    }
    QGroupBox {
        border-radius: 6px;
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

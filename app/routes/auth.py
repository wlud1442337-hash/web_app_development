from flask import Blueprint, render_template, request, redirect, url_for, session

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """處理登入表單與認證"""
    pass

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """處理註冊表單與創建會員"""
    pass

@auth_bp.route('/logout', methods=['GET'])
def logout():
    """清除登入狀態並登出"""
    pass

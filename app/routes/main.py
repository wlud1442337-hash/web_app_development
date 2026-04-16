from flask import Blueprint, render_template, request, redirect, url_for, session

main_bp = Blueprint('main', __name__)

@main_bp.route('/', methods=['GET'])
def index():
    """顯示首頁與抽籤入口"""
    pass

@main_bp.route('/draw', methods=['POST'])
def draw():
    """執行隨機抽籤，並在登入狀態下存入資料庫，隨後重導向至結果頁"""
    pass

@main_bp.route('/result/<int:id>', methods=['GET'])
def result(id):
    """檢視指定抽籤紀錄的結果"""
    pass

@main_bp.route('/donate', methods=['GET', 'POST'])
def donate():
    """處理香油錢模擬捐款表單"""
    pass

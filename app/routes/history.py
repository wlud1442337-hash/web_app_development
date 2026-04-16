from flask import Blueprint, render_template, session, redirect

history_bp = Blueprint('history', __name__)

@history_bp.route('/history', methods=['GET'])
def history():
    """列出目前使用者的過往抽籤紀錄"""
    pass

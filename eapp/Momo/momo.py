from flask import Flask, redirect, request, jsonify, render_template
import requests, uuid, hmac, hashlib
import os
from eapp.dao import PaymentDao
from eapp.models.Payment import PaymentStatus
from eapp import db

app = Flask(__name__)

# ===== MOMO SANDBOX CONFIG =====
PARTNER_CODE = "MOMO"
ACCESS_KEY = os.getenv("ACCESS_KEY")
SECRET_KEY = os.getenv("SECRET_KEY")
ENDPOINT = "https://test-payment.momo.vn/v2/gateway/api/create"

RETURN_URL = "https://e49b46b65ec5.ngrok-free.app/momo/return"
IPN_URL = "https://e49b46b65ec5.ngrok-free.app/momo/ipn"


def create_signature(data, secret):
    return hmac.new(
        secret.encode(),
        data.encode(),
        hashlib.sha256
    ).hexdigest()



def created_pay(momo_order_id, total):
    request_id = str(uuid.uuid4())
    raw_signature = (
        f"accessKey={ACCESS_KEY}"
        f"&amount={int(total)}"
        f"&extraData="
        f"&ipnUrl={IPN_URL}"
        f"&orderId={momo_order_id}"
        f"&orderInfo=Test MoMo Flask"
        f"&partnerCode={PARTNER_CODE}"
        f"&redirectUrl={RETURN_URL}"
        f"&requestId={request_id}"
        f"&requestType=captureWallet"
    )

    signature = create_signature(raw_signature, SECRET_KEY)

    payload = {
        "partnerCode": PARTNER_CODE,
        "accessKey": ACCESS_KEY,
        "requestId": request_id,
        "amount": total,
        "orderId": momo_order_id,
        "orderInfo": "Test MoMo Flask",
        "redirectUrl": RETURN_URL,
        "ipnUrl": IPN_URL,
        "extraData": "",
        "requestType": "captureWallet",
        "signature": signature,
        "lang": "vi"
    }
    res = requests.post(ENDPOINT, json=payload).json()
    return res


def TransactionStatus():
    order_id = str(uuid.uuid4())
    request_id = str(uuid.uuid4())
    raw_signature = (
        f"accessKey={ACCESS_KEY}"
        f"&orderId={order_id}"
        f"&partnerCode={PARTNER_CODE}"
        f"&requestId={request_id}"
    )
    signature = hmac.new(
        SECRET_KEY.encode(),
        raw_signature.encode(),
        hashlib.sha256
    ).hexdigest()

    payload = {
        "partnerCode": PARTNER_CODE,
        "accessKey": ACCESS_KEY,
        "requestId": request_id,
        "orderId": order_id,
        "signature": signature,
        "lang": "vi"
    }
    res = requests.post(
        "https://test-payment.momo.vn/v2/gateway/api/query",
        json=payload
    ).json()
    return jsonify(res)


def momo_ipn():
    print(1)
    data = request.json
    print("data:", data)
    order_id = data.get("orderId")
    result_code = data.get("resultCode")
    trans_id = data.get("transId")
    print("rscode", result_code)
    payment = PaymentDao.get_by_momo_id(order_id)
    if not payment:
        return jsonify({"message": "payment not found"}), 404

    if result_code == 0:
        payment.status =  PaymentStatus.success
        payment.momo_trans_id = trans_id
    else:
        payment.status = "failed"

    db.session.commit()
    return jsonify({"message": "OK"})

def momo_return():
    return render_template('page/cart.html')
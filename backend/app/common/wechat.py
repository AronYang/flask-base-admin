# -*- coding:utf-8 -*-
# Author:      LiuSha
import base64
import hashlib
import random
import socket
import string
import struct
import time
import xml.etree.cElementTree as ElementTree
from xml.etree.cElementTree import Element

from Crypto.Cipher import AES


class CryptSuccess(object):
    OK = 0


class CryptFailed(object):
    VALIDATE_SIGNATURE = -40001
    PARSE_XML = -40002
    COMPUTE_SIGNATURE = -40003
    ILLEGAL_AES_KEY = -40004
    VALIDATE_CORP_ID = -40005
    ENCRYPT_AES = -40006
    DECRYPT_AES = -40007
    ILLEGAL_BUFFER = -40008
    ENCODE_BASE64 = -40009
    DECODE_BASE64 = -40010
    GEN_RETURN_XML = -40011


class FormatException(Exception):
    pass


def throw_exception(message, exception_class=FormatException):
    """
    my define raise exception function
    """
    raise exception_class(message)


def get_sha1(token, timestamp, nonce, encrypt):
    """
    用SHA1算法生成安全签名

    @:param token:  票据
    @:param timestamp: 时间戳
    @:param encrypt: 密文
    @:param nonce: 随机字符串
    @:return: 安全签名
    """

    try:
        sortlist = [token, timestamp, nonce, encrypt]
        sortlist.sort()
        sha = hashlib.sha1()
        sha.update("".join(sortlist).encode())
        return CryptSuccess.OK, sha.hexdigest()
    except Exception as err:
        print(err)
        return CryptFailed.COMPUTE_SIGNATURE, None


class XMLParse(object):
    """
    提供提取消息格式中的密文及生成回复消息格式的接口
    """

    #: XML 消息模板
    AES_TEXT_RESPONSE_TEMPLATE = """<xml>
<Encrypt><![CDATA[%(msg_encrypt)s]]></Encrypt>
<MsgSignature><![CDATA[%(msg_signaturet)s]]></MsgSignature>
<TimeStamp>%(timestamp)s</TimeStamp>
<Nonce><![CDATA[%(nonce)s]]></Nonce>
</xml>"""

    @staticmethod
    def extract_encrypt_message(xmltext):
        """
        提取出xml数据包中的加密消息

        @:param xmltext: 待提取的xml字符串
        @:return: 提取出的加密消息字符串
        """
        try:
            xml_tree = ElementTree.fromstring(xmltext)
            encrypt = xml_tree.find("Encrypt")
            touser_name = xml_tree.find("ToUserName")

            return CryptSuccess.OK, encrypt.text, touser_name.text
        except Exception as err:
            print(err)
            return CryptFailed.PARSE_XML, None, None

    @staticmethod
    def extract_message(xmltext):
        """
        提取出xml数据包中的消息

        @:param xmltext: 待提取的xml字符串
        @:return: 提取出的加密消息字符串
        """
        try:
            xml_tree = ElementTree.fromstring(xmltext)

            message_id = xml_tree.find("MsgId")
            message_type = xml_tree.find("MsgType")
            to_user_name = xml_tree.find("ToUserName")
            content = xml_tree.find("Content")
            from_username = xml_tree.find("FromUserName")
            create_time = xml_tree.find("CreateTime")
            event_type = xml_tree.find("Event")
            event_key = xml_tree.find("EventKey")
            media_id = xml_tree.find("MediaId")

            return CryptSuccess.OK, {
                "id": message_id.text if isinstance(message_id, Element) else '',
                "type": message_type.text if isinstance(message_type, Element) else '',
                "to": to_user_name.text if isinstance(to_user_name, Element) else '',
                "from": from_username.text if isinstance(from_username, Element) else '',
                "content": content.text if isinstance(content, Element) else '',
                "create_time": create_time.text if isinstance(create_time, Element) else '',
                "event": event_type.text if isinstance(event_type, Element) else '',
                "event_key": event_key.text if isinstance(event_key, Element) else '',
                "media_id": media_id.text if isinstance(media_id, Element) else '',
            }
        except Exception as err:
            print(err)
            return CryptFailed.PARSE_XML, None

    def generate(self, encrypt, signature, timestamp, nonce):
        """
        生成xml消息

        @:param encrypt: 加密后的消息密文
        @:param signature: 安全签名
        @:param timestamp: 时间戳
        @:param nonce: 随机字符串
        @:return: 生成的xml字符串
        """
        resp_dict = {
            'msg_encrypt': encrypt,
            'msg_signaturet': signature,
            'timestamp': timestamp,
            'nonce': nonce
        }

        resp_xml = self.AES_TEXT_RESPONSE_TEMPLATE % resp_dict
        return resp_xml


class PKCS7Encoder(object):
    """
    提供基于PKCS7算法的加解密接口
    """

    block_size = 32

    def encode(self, text):
        """
        对需要加密的明文进行填充补位

        @:param text: 需要进行填充补位操作的明文
        @:return: 补齐明文字符串
        """
        text_length = len(text)

        #: 计算需要填充的位数
        amount_to_pad = self.block_size - (text_length % self.block_size)
        if amount_to_pad == 0:
            amount_to_pad = self.block_size

        #: 获得补位所用的字符
        pad = chr(amount_to_pad)
        return text + pad * amount_to_pad

    @staticmethod
    def decode(decrypted):
        """
        删除解密后明文的补位字符

        @param decrypted: 解密后的明文
        @return: 删除补位字符后的明文
        """
        pad = ord(decrypted[-1])
        if pad < 1 or pad > 32:
            pad = 0

        return decrypted[:-pad]


class Prpcrypt(object):
    """
    提供接收和推送给企业微信消息的加解密接口
    """

    def __init__(self, key):

        #: self.key = base64.b64decode(key+"=")
        self.key = key

        #: 设置加解密模式为AES的CBC模式
        self.mode = AES.MODE_CBC

    @staticmethod
    def get_random_str():
        """
        随机生成16位字符串

        @return: 16位字符串
        """
        rule = string.ascii_letters + string.digits
        return "".join(random.sample(rule, 16))

    def encrypt(self, text, corpid):
        """
        对明文进行加密
        @:param text: 需要加密的明文
        @:param corpid: 企业应用 ID
        @:return: 加密得到的字符串
        """

        #: 16位随机字符串添加到明文开头
        text = self.get_random_str() + struct.pack("I", socket.htonl(len(text))).decode() + text + corpid

        #: 使用自定义的填充方式对明文进行补位填充
        pkcs7 = PKCS7Encoder()
        text = pkcs7.encode(text)

        #: 加密
        cryptor = AES.new(self.key, self.mode, self.key[:16])
        try:
            ciphertext = cryptor.encrypt(text)
            # 使用BASE64对加密后的字符串进行编码
            return CryptSuccess.OK, base64.b64encode(ciphertext)
        except Exception as err:
            print(err)
            return CryptFailed.GEN_RETURN_XML, None

    def decrypt(self, text, corpid):
        """
        对解密后的明文进行补位删除
        @:param text: 密文
        @:param corpid: 企业应用 ID
        @:return: 删除填充补位后的明文
        """

        try:
            cryptor = AES.new(self.key, self.mode, self.key[:16])

            #: 使用BASE64对密文进行解码，然后AES-CBC解密
            plain_text = cryptor.decrypt(base64.b64decode(text))
        except Exception as err:
            print(err)
            return CryptFailed.DECRYPT_AES, None

        try:
            pad = plain_text[-1]
            if isinstance(pad, str):
                pad = ord(pad)

            #: 去除16位随机字符串
            content = plain_text[16:-pad]
            xml_len = socket.ntohl(struct.unpack("I", content[:4])[0])

            xml_content = content[4:xml_len + 4]
            from_corpid = content[xml_len + 4:]
        except Exception as err:
            print(err)
            return CryptFailed.ILLEGAL_BUFFER, None

        if isinstance(from_corpid, bytes):
            from_corpid = from_corpid.decode()

        if isinstance(xml_content, bytes):
            xml_content = xml_content.decode()

        if from_corpid != corpid:
            return CryptFailed.VALIDATE_CORP_ID, None

        return CryptSuccess.OK, xml_content


class MessageCrypt(object):
    """
    @:param token: 企业微信后台，开发者设置的Token
    @:param encoding_aes_key: 企业微信后台，开发者设置的EncodingAESKey
    @:param corp_id: 企业号的CorpId
    """

    # noinspection PyBroadException
    def __init__(self, token, encoding_aes_key, corp_id):
        try:
            self.key = base64.b64decode(encoding_aes_key + "=")
            assert len(self.key) == 32
        except Exception as err:
            throw_exception("[error]: EncodingAESKey unvalid, %s!" % err, FormatException)

        self.token = token
        self.corp_id = corp_id

    def verify_url(self, msg_signature, timestamp, nonce, echostr):
        """
        验证URL
        @param msg_signature: 签名串，对应URL参数的 msg_signature
        @param timestamp: 时间戳，对应URL参数的 timestamp
        @param nonce: 随机串，对应URL参数的 nonce
        @param echostr: 随机串，对应URL参数的 echostr
        @return：成功0，失败返回对应的错误码
        """

        ret, signature = get_sha1(self.token, timestamp, nonce, echostr)
        if ret != 0:
            return ret, None

        if not signature == msg_signature:
            return CryptFailed.VALIDATE_SIGNATURE, None

        pc = Prpcrypt(self.key)
        ret_code, reply_echo_str = pc.decrypt(echostr, self.corp_id)
        return ret_code, reply_echo_str

    def encrypt_message(self, reply_message, nonce, timestamp=None):
        """
        将企业回复用户的消息加密打包
        @:param reply_message: 企业号待回复用户的消息，xml 格式的字符串
        @:param nonce: 随机串，可以自己生成，也可以用 URL 参数的 nonce
        @:param timestamp: 时间戳，可以自己生成，也可以用URL参数的timestamp,如为None则自动用当前时间

        encrypt_message: 加密后的可以直接回复用户的密文，包括msg_signature, timestamp, nonce, encrypt的xml格式的字符串,
        @:return：成功0，sEncryptMsg,失败返回对应的错误码None
        """
        pc = Prpcrypt(self.key)
        ret, encrypt = pc.encrypt(reply_message, self.corp_id)
        if ret != 0:
            return ret, None

        if timestamp is None:
            timestamp = str(int(time.time()))

        #: 生成安全签名
        ret_code, signature = get_sha1(self.token, timestamp, nonce, encrypt)
        if ret_code != 0:
            return ret_code, None

        xml_parse = XMLParse()
        return ret_code, xml_parse.generate(encrypt, signature, timestamp, nonce)

    def decrypt_message(self, post_data, msg_signature, timestamp, nonce):
        """
        检验消息的真实性，并且获取解密后的明文
        @:param msg_signature: 签名串，对应URL参数的 msg_signature
        @:param timestamp: 时间戳，对应URL参数的 timestamp
        @:param nonce: 随机串，对应URL参数的 nonce
        @:param post_data: 密文，对应 POST 请求的数据

        xml_content: 解密后的原文，当 return 返回 0 时有效
        @:return: 成功0，失败返回对应的错误码
        验证安全签名
        """
        xml_parse = XMLParse()
        ret_code, encrypt, touser_name = xml_parse.extract_encrypt_message(post_data)

        if ret_code != 0:
            return ret_code, None

        ret_code, signature = get_sha1(self.token, timestamp, nonce, encrypt)

        if ret_code != 0:
            return ret_code, None

        if not signature == msg_signature:
            return CryptFailed.VALIDATE_SIGNATURE, None

        pc = Prpcrypt(self.key)
        ret_code, xml_content = pc.decrypt(encrypt, self.corp_id)

        return ret_code, xml_content

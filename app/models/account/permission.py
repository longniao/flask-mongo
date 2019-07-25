# -*- coding: utf-8 -*-


class Permission:
    POST_TXT = 0x01
    POST_IMAGE = 0x02
    POST_AUDIO = 0x03
    POST_VIDEO = 0x04
    POST_POLL = 0x05
    POST_ASK = 0x06
    POST_ACTIVITY = 0x07
    POST_TRADE = 0x08
    POST_HOUSE = 0x09

    COMMENT = 0x11

    EDIT = 0x21

    FOLLOW = 0x31

    COLLECT = 0x41

    SHARE = 0x51

    UP = 0x61
    DOWN = 0x62

    CONTENT_AUDIT = 0x91
    CONTENT_MANAGE = 0x92
    ACCOUNT_MANAGE = 0x93
    ADMINISTER = 0x99

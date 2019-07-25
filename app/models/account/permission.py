# -*- coding: utf-8 -*-


class Permission:
    post_text = True
    post_image = True
    post_audio = True
    post_video = True
    post_poll = True
    post_ask = True
    post_activity = True
    post_trade = True
    post_house = True

    action_visit = True
    action_search = True
    action_invite = True
    action_comment = True
    action_follow = True
    action_collect = True
    action_share = True
    action_up = True
    action_down = True

    content_audit = False
    content_manage = False
    account_manage = False

    administer = False

    def to_json(self):
        return {
            "post_text": self.post_text,
            "post_image": self.post_image,
            "post_audio": self.post_audio,
            "post_video": self.post_video,
            "post_poll": self.post_poll,
            "post_ask": self.post_ask,
            "post_activity": self.post_activity,
            "post_trade": self.post_trade,
            "post_house": self.post_house,

            "action_visit": self.action_visit,
            "action_search": self.action_search,
            "action_invite": self.action_invite,
            "action_comment": self.action_comment,
            "action_follow": self.action_follow,
            "action_collect": self.action_collect,
            "action_share": self.action_share,
            "action_up": self.action_up,
            "action_down": self.action_down,

            "content_audit": self.content_audit,
            "content_manage": self.content_manage,
            "account_manage": self.account_manage,

            "administer": self.administer,
        }
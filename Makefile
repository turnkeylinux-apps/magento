COMMON_OVERLAYS = github-latest-release
COMMON_CONF = apache-credit
CREDIT_LOCATION = ~ "^/(?!(admin|index.php/admin|js/tiny_mce))"
define CREDIT_STYLE_EXTRA
#turnkey-credit {
    color: #FFF;
}
#turnkey-credit a {
    color: #DDD;
}
.footer {
    padding: 10px;
}
endef

include $(FAB_PATH)/common/mk/turnkey/composer.mk
include $(FAB_PATH)/common/mk/turnkey/lamp.mk
include $(FAB_PATH)/common/mk/turnkey.mk

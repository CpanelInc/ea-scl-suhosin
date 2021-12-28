OBS_PROJECT := EA4
scl-php56-php-suhosin-obs : DISABLE_BUILD += repository=CentOS_8
scl-php55-php-suhosin-obs : DISABLE_BUILD += repository=CentOS_8
scl-php54-php-suhosin-obs : DISABLE_BUILD += repository=CentOS_8
OBS_PACKAGE := scl-suhosin
include $(EATOOLS_BUILD_DIR)obs-scl.mk

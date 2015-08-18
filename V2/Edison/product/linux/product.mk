# $@ 目标文件
# $^ 全部依赖文件
# $< 第一个依赖文件

INC+= -I$(ROOTDIR)/product/linux 

product: $(TARGET)/$(BIN)

TAGET_FILES := $(ROOTDIR)/product/linux/main.c \
$(ROOTDIR)/product/linux/x86_drv.c \
$(ROOTDIR)/platform/gmcu/core_gagent.c \
$(ROOTDIR)/iof/iof_hook.c

#target file
$(TARGET)/$(BIN):
	$(CC) $(CFLAGS) $(TAGET_FILES) $(LIBTARGET_FILES) $(INC) -o $(TARGET)/$(BIN)
	cp $(ROOTDIR)/Projects/linux/rgb $(TARGET)/rgb
	cp $(ROOTDIR)/Projects/linux/pwm $(TARGET)/pwm
	cp $(ROOTDIR)/Projects/linux/yuv $(TARGET)/yuv
	cp $(ROOTDIR)/Projects/linux/tclient.py $(TARGET)/tclient.py
	cp $(ROOTDIR)/Projects/linux/init_DIG.sh $(TARGET)/init_DIG.sh
	cp $(ROOTDIR)/Projects/linux/set_DIG.sh $(TARGET)/set_DIG.sh
	cp $(ROOTDIR)/Projects/linux/read_DIG.sh $(TARGET)/read_DIG.sh
	cp $(TARGET)/gagent_x86_debug /home/root/gagent_x86_debug
	chmod 777 $(TARGET)/yuv
	chmod 777 $(TARGET)/init_DIG.sh
	chmod 777 $(TARGET)/set_DIG.sh
	chmod 777 $(TARGET)/read_DIG.sh
	chmod 777 /home/root/gagent_x86_debug
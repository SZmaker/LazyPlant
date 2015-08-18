#ifndef _GAGENT_CLOUD_H_
#define _GAGENT_CLOUD_H_

#define FIRMWARE_LEN            8

typedef struct
{
    unsigned int pingTime;      /* ͬmqtt ������ʱ, ��ʱ������������ */
    unsigned int loseTime;      /* ������ʧ��������  */

    char *otaUrlHttpCont;       /* ����ota firmware���ص�ַ,����HTTP get��content */
    int ota_fid;                /* ota firmware id,���ƶ˻�ȡ  */
}GAGENT_CLOUD_TYPE;

extern GAGENT_CLOUD_TYPE Gagent_Cloud_status;

unsigned char mqtt_num_rem_len_bytes(const unsigned char *buf);
unsigned short mqtt_parse_rem_len(const unsigned char* buf);

extern void GAgent_Cloud_Timer(void);

#endif



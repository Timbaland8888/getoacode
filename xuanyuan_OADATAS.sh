#!/bin/bash
#Arthor:Timbaland
#Function:get oa datas
#Date：2017-08-18

cd /oa/Local_OA

python /oa/Local_OA/xuanyuan_OADATAS.py > /dev/null 2>&1
python xuanyuan_update_umuser.py > /dev/null 2>&1


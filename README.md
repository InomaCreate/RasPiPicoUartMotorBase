# 概要
raspiPICO+KITRONIK-5331を使ったDCモーター制御車両ベースです。  
![RasPiPicoUartMotorBase_image4](https://github.com/user-attachments/assets/601968ce-726d-4a36-ae15-d4004a7905f6)

UART通信を使い、モーター駆動指示、モーター回転数を取得します。
![RasPiPicoUartMotorBase_image3](https://github.com/user-attachments/assets/7c371001-c640-49a7-a114-c1c4d8a5f2f6)


## UART通信仕様
RasPiPicoUartMotorBaseとマイコン等の制御用ボードをUARTで接続し、以下のコマンドをUARTで通知することでDCモーターを駆動させることが可能です。  
また、モーターの回転数（rpm)の情報をUARTで受信することができます。

### UARTコマンド
| UARTコマンド(制御ボード→RasPiPicoUartMotorBase) | 説明 |
|:---|:---:|
|start${"v_r": 右モーター速度指示値, "v_l":左モーター速度指示値} |モーター駆動指示   |  
|emergency_stop|モーター停止 |

※速度指示値は0〜100 ※終端に改行コードCRLF(\r\n)を入れること

| UART応答(制御ボード←RasPiPicoUartMotorBase) | 説明 |
|:---|:---:|
|{"rpm_l":左モーター回転数(rpm),"rpm_r":右モーター回転数(rpm)} |モーター回転数応答 |  

## 準備
### 必要なもの
- Raspberry Pi Pico
- Raspberry Pi Pico用Kitronikモータードライバーボード(KITRONIK-5331)
- エンコーダ付きDCモーター×2個
  - 動作実績：DC 12v モーター エンコーダ付き ギアモーター マウントブラケット付き 65mm(130rpm)
- モーター駆動用バッテリ(モーター電圧に応じて準備）
  
### ソフトウェア
※Raspberry Pi Pico開発環境はThonnyを使用
https://thonny.org/

1. Micro Pythonのファームウェアをセットアップしてください。  
以下サイト参照。  
https://www.marutsu.co.jp/pc/static/large_order/zep/m-z-picoled-da1?srsltid=AfmBOorvtQBPDclVyJtAbuTcil99_cpVNFvaeHsgTcH8kHxA0RaH-YSx  

3. Kitronik用のドライバー(PicoMotorDriver.py)をRaspberry Pi Picoに保存します。    
以下参照。  
https://github.com/KitronikLtd/Kitronik-Pico-Motor-Driver-Board-MicroPython

4. RasPiPicoSource内にあるmain.pyをRaspberry Pi Picoに保存します。  
https://github.com/InomaCreate/RasPiPicoUartMotorBase/blob/main/RasPiPicoSource/main.py

### ハードウェア
1. raspiPICO+KITRONIK-5331を接続し、UART用線を出します。（要ハンダ付け）  
UART1 TX:GPIO4(PIN6), UART1 RX:GPIO5(PIN7), GND(PIN8)から線を出します。  

2. 以下のようにDCモーターと接続します。  
![RasPiPicoUartMotorBase_image2new](https://github.com/user-attachments/assets/04025d7a-b2d4-4569-aa64-365379b41678)

実際の配線写真↓  
![RasPiPicoUartMotorBase_image1](https://github.com/user-attachments/assets/9220c1c1-db41-4a36-9869-cbe299753796)



## サンプルプログラム
### 動作実績：
- Raspberry Pi 5（Ubuntu24.04)  
以下、Raspberry Pi 5（Ubuntu24.04)を使ったサンプルプログラムのセットアップ、実行方法を記載します。  

### セットアップ：
1. Raspberry Pi5のUART通信を有効にする  
   1-1. /boot/firmware/config.txtを編集し、以下を追加します。  
   ```enable_uart=1```  
   ```dtoverlay=uart0```  

   1-2. Raspberry Pi5を再起動します  
   ```sudo reboot```
    
   1-3. 再起動後、以下コマンドでuartが有効になっているか確認します。  
   ```sudo dmesg | grep ttyAMA```  
   ttyAMA0が有効になっている場合、以下のピンがUART信号のピンです。  
   ttyAMA0・・・PIN8：GPIO14（TxD）/ PIN10：GPIO15(RxD)  

   1-4. RasPiPicoUartMotorBaseのUART線をRaspberry Pi5のUARTピンと接続します。
   ![RasPiPicoUartMotorBase_image5](https://github.com/user-attachments/assets/a5f7ab8e-4351-4c18-8c67-189dea765469)
   

   
3. Raspberry Pi5に必要なパッケージのインストール  
以下のコマンドで、サンプルプログラムを実行するために必要なパッケージをインストールします  
```sudo apt update```  
```sudo apt install libncurses5-dev libncursesw5-dev```  
```pip3 install pyserial```  


### 実行方法：
セットアップしたRaspberry Piでサンプルプログラムを動かします。  
#### モーター駆動用サンプルプログラム
以下スクリプトを実行すると、モーター駆動用のサンプルプログラムが起動します。  
キーを通知すると、前進、後進、モーター速度変更などを行います。（以下表参照）  
```python3 sample_motor_send.py```  

| キー | 動作 |
|:---|:---:|
| i | 前進 |
| k | 後進 |
| s | 右モーター速度UP(+5) |
| a | 左モーター速度UP(+5) |
| x | 右モーター速度DOWN(-5) |
| z | 左モーター速度DOWN(-5) |
| e | モーター停止 |
| q | プログラム終了 |



#### モーター回転数受信サンプルプログラム
以下スクリプトを実行すると、モーター回転数受信のサンプルプログラムが起動します。  
```python3 sample_rcv_rpm.py``` 

## 3Dデータ
3Dデータ(stlファイル）もGitHubにUPしました。必要に応じて3Dプリンターで印刷してご使用ください。  
[https://github.com/InomaCreate/RasPiPicoUartMotorBase/tree/main/3D-data](https://github.com/InomaCreate/RasPiPicoUartMotorBase/blob/main/3D-data/RasPiPicoUartMotorBase_body-Body.stl)


以下のように、Raspberry Pi Picoや電池ボックス、モーター、キャスターを取り付けれるようにしております。
![github_image-06](https://github.com/user-attachments/assets/e641a84a-373e-4542-b344-a977cca06a89)
キャスターは、ホームセンターで買った直径38mmのものです。  
![github_image-07](https://github.com/user-attachments/assets/fa3f5e5d-8827-4ea0-8a7e-6b4a5467271e)

モーターのマウントは、「DC 12v モーター エンコーダ付き ギアモーター マウントブラケット付き 65mm(130rpm)」に付属されていたマウントブランケットをそのまま使用しています。  
![github_image-08](https://github.com/user-attachments/assets/a013b6a9-5359-4d2f-8b34-fa3b3e6589ed)






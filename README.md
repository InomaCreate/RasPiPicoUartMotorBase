# 概要
ラズパイPICO+KITRONIK-5331を使ったDCモーター制御車両ベース  
UART通信を使い、モーター駆動指示、モーター回転数を取得します。

## UART通信仕様
RasPiPicoUartMotorBaseとマイコン等の制御用ボードをUARTで接続し、以下のコマンドをUARTで通知することでDCモーターを駆動させることが可能です。  
また、モーターの回転数（rpm)の情報をUARTで受信することができます。

### UARTコマンド
| UARTコマンド(制御ボード→RasPiPicoUartMotorBase) | 説明 |
|:---|:---:|
|start${"v_r": 右モーター速度指示値, "v_l":左モーター速度指示値} |モーター駆動指示   |  

※速度指示値は0〜100 ※終端に改行コードCRLF(\r\n)を入れること

| UART応答(制御ボード←RasPiPicoUartMotorBase) | 説明 |
|:---|:---:|
|{"rpm_l":左モーター回転数(rpm),"rpm_r":右モーター回転数(rpm)} |モーター回転数応答 |  

## 準備
### 必要なもの
- Raspberry Pi Pico
- Raspberry Pi Pico用Kitronikモータードライバーボード(KITRONIK-5331)
- エンコーダ付きDCモーター×2個
  - 動作実績：encoder, FTVOGUE モーター　DC6V 50RPM
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
※図準備中・・  

## サンプルプログラム
準備中です・・・・  




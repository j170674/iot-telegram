/***************************************************************
 *         _____
 *        |   | |
 *        |_|___|
 *      __ _____ _____ _____    _____           _         _
 *   __|  |  _  |     |   __|  |  _  |___ ___  |_|___ ___| |_
 *  |  |  |     |  |  |__   |  |   __|  _| . | | | -_|  _|  _|  _
 *  |_____|__|__|_____|_____|  |__|  |_| |___|_| |___|___|_|   |_|
 *                                           |___|
 *                                                     Version 1.0
 ****************************************************************/
/*************************************/
/*          INCLUDES                 */
/**************************************/
#include <SPI.h>
#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <Adafruit_GFX.h>
#include <Adafruit_PCD8544.h>
#include "DHT.h"        // including the library of DHT11 temperature and humidity sensor
/*************************************/
/*          DEFINES                  */
/*************************************/
#define DHTTYPE DHT11   // DHT 11

/*-------------- WIFI ---------------*/
//#define WLAN_SSID  "aula-ic3" // rede wifi
#define WLAN_SSID  "Jaonet" // rede wifi
#define WLAN_PASSWORD  "iotic@2019" // senha da rede wifi
/*------------- BROKER ---------------*/
#define BROKER_MQTT  "mqtt.demo.konkerlabs.net" // ip/host do broker
#define BROKER_PORT  1883 // porta do broker
/*************************************/
/*          PROTOTYPES               */
/**************************************/
void  initSerial();
void  initWiFi();
void  initMQTT();
void  initDisplay();
void  printDisplay(String msg);
void  defaultScreen();
float getTemperatura();
float getUmidade();
float getLuminosidade();
void  telegramMessage(String msg);
void  mqtt_callback(char* topic, byte* payload, unsigned int length);
/*************************************/
/*          GLOBAL VARS              */
/**************************************/
WiFiClient espClient;
PubSubClient MQTT(espClient); // instancia o mqtt
DHT dht(D4, DHTTYPE);
/**************************************/
/*          DISPLAY PINS SETUP        */
/**************************************/
/* pin D8 - Serial clock out (SCLK)   */
/* pin D7- Serial data out (DIN)      */
/* pin D6 - Data/Command select (D/C) */
/* pin D5 - LCD chip select (CS)      */
/* pin D2 - LCD reset (RST)           */
/**************************************/
Adafruit_PCD8544 display = Adafruit_PCD8544(D8, D7, D6, D5, D2);

/**************************************/
/*                SETUP               */
/**************************************/
void setup() {
    dht.begin();
    initSerial();
    initWiFi();
    initMQTT();
    initDisplay();
    defaultScreen();

}

/**************************************/
/*                LOOP                */
/**************************************/
void loop() {
    if (!MQTT.connected()) {
        reconnectMQTT();
    }
    recconectWiFi();
    MQTT.loop();
}


/*=====================================*/
/*     PROTOTYPES IMPLEMENTATIONS     */
/*====================================*/

/**************************************/
/*     INTITIAL CONFIGURATIONS FUNC   */
/**************************************/
void initSerial() {
    Serial.begin(115200);
}

void initWiFi() {
    delay(10);
    Serial.println("Conectando-se em: " + String(WLAN_SSID));

    WiFi.begin(WLAN_SSID, WLAN_PASSWORD);
    while (WiFi.status() != WL_CONNECTED) {
        delay(100);
        Serial.print(".");
    }
    Serial.println();
    Serial.print("Conectado na Rede " + String(WLAN_SSID) + " | IP => ");
    Serial.println(WiFi.localIP());
}

void initDisplay(){
    display.begin();
    display.setContrast(50);
    display.clearDisplay();
    display.setTextSize(0);
    display.setTextColor(BLACK, WHITE);
    display.setCursor(0,0);
}

void defaultScreen(){
    display.setCursor(0,0);
    display.clearDisplay();
    display.setTextSize(2);
    display.println("  IOT");
    display.setTextSize(1);
    display.println("   TELEGRAM");
    if (MQTT.connected()){
        display.print("   \n\nc.c");
    }
    display.display();
}


// Funcão para se conectar ao Broker MQTT
void initMQTT() {
    MQTT.setServer(BROKER_MQTT, BROKER_PORT);
    MQTT.setCallback(mqtt_callback);
}

void reconnectMQTT() {
    while (!MQTT.connected()) {
        Serial.println("Tentando se conectar ao Broker MQTT: " + String(BROKER_MQTT));
        if (MQTT.connect("JaoJaoDevice1","j9j976fenpqs", "IjzR8T18LJty")) {
            Serial.println("Conectado");
            MQTT.subscribe("data/j9j976fenpqs/sub/in");
        } else {
            Serial.println("Falha ao Reconectar");
            Serial.println("Tentando se reconectar em 2 segundos");
            delay(2000);
        }
    }
}

void recconectWiFi() {
    while (WiFi.status() != WL_CONNECTED) {
        delay(100);
        Serial.print(".");
    }
}
/**************************************/
/*        MQTT CALLBACKS SETUP        */
/**************************************/
void mqtt_callback(char* topic, byte* payload, unsigned int length) {

    String message;

    for (int i = 0; i < length; i++) {
        char c = (char)payload[i];
        message += c;
    }
    Serial.println("Tópico => " + String(topic) + " | Valor => " + String(message));
    if (message == "\"temp\""){

        String resp = String(getTemperatura());
        if (resp.equals("nan"))
            resp = "Sensor Failed";
        else
            resp += " C";
        int len = resp.length() +1;
        char buff[len];
        memset(buff,'\0',sizeof(buff));
        resp.toCharArray(buff, len);
        MQTT.publish("data/j9j976fenpqs/pub/out", buff); //1
        printDisplay("Temperatura:\n"+resp);
    }
    else if (message == "\"hum\""){
        String resp = String(getUmidade());
        if (resp.equals("nan"))
            resp = "Sensor Failed";
        else
            resp += " %";
        int len = resp.length() +1;
        char buff[len];
        memset(buff,'\0',sizeof(buff));
        //      sprintf(buff, sizeof(buff)-1, "%s", resp.c_str() );
        resp.toCharArray(buff, len);
        MQTT.publish("data/j9j976fenpqs/pub/out", buff); //2
        printDisplay("Umidade:\n"+resp);
    }
    else if (message == "\"light\""){
        String resp = String(getLuminosidade());
        if (resp.equals("nan"))
            resp = "Sensor Failed";
        else
            resp += " %";
        int len = resp.length() +1;
        char buff[len];
        memset(buff,'\0',sizeof(buff));
        resp.toCharArray(buff, len);
        MQTT.publish("data/j9j976fenpqs/pub/out", buff); //3
        printDisplay("Luminosidade:\n"+resp);
    }
    else if (message.indexOf("\"display$") == 0){
        telegramMessage(message);
    }
    else {
        Serial.println("Comando invalido => " + String(message));
    }
    defaultScreen();
    Serial.flush();
}

/**************************************/
/*     SENSORS ACQUISITIONS FUNC      */
/**************************************/
float getTemperatura(){
    return dht.readTemperature();

}
float getUmidade(){
    return dht.readHumidity();
}
float getLuminosidade(){
    return (1-analogRead(A0)/1024.0)*100.0;
}

/**************************************/
/*            DISPLAY  FUNC           */
/**************************************/
void telegramMessage(String msg){
    msg = msg.substring(9,msg.length()-1); //remove display command
    msg.replace("\\n","\n");
    //String display_msg;
    Serial.println(">> BEGIN "+msg);
    printDisplay(msg);
    Serial.println(msg+"<< END");
}
void printDisplay(String msg){
    Serial.println("Display =>"+ msg);
    display.setCursor(0,0);
    display.clearDisplay();
    display.print(msg);
    display.display();
    delay(3000);

}

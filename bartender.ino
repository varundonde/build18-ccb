// Drink Pins
const int drink1 = 3; 
const int drink2 = 4; 
const int drink3 = 5; 
const int drink4 = 6; 
const int drink5 = 7; 
const int drink6 = 8; 

const int BAUD_RATE = 9600;


// Placeholder Function for converting ratios to dispensing times
int value_to_delay_time(int value) {
    // Placeholder value
    return value * 500; 
}

// Dispensing Function 
void dispense(int[] ratio) {
    for (int pump = 3; pump <= 8; pump++) {
        digitalWrite(pump, HIGH); 
        delay(value_to_delay_time(ratios[pump - 3]));
        digitalWrite(pump, LOW);
        delay(value_to_delay_time(ratios[pump - 3]));
    }
}
    



    // for (int i = 0; i < value_to_dispensing_time(ratios[pin]); i++) {
    //     digitalWrite(pin, HIGH); 
    //     delayMicroseconds(DELAY_BEFORE_NEXT_DRINK);
    //     digitalWrite(pin, LOW);
    //     delayMicroseconds(DELAY_BEFORE_NEXT_DRINK);
    // }

void setup() {
    // Set up the pins
    pinMode(drink1, OUTPUT);
    pinMode(drink2, OUTPUT);
    pinMode(drink3, OUTPUT);
    pinMode(drink4, OUTPUT);
    pinMode(drink5, OUTPUT);
    pinMode(drink6, OUTPUT);
    // Set up serial connection speed
    Serial.begin(BAUD_RATE); 
    // Include some delay before starting the dispensing
    delay(1000); 
}

void loop() {
    while (!Serial.available());
    
    String inputString = Serial.readStringUntil('\n');
    int ratios[6]; // Assuming 6 pumps
    int index = 0;
    
    // Parse the input string
    char* str = const_cast<char*>(inputString.c_str());
    char* token = strtok(str, ",");
    
    while (token != NULL && index < 6) {
        // atoi to convert string to integer
        ratios[index] = atoi(token);
        token = strtok(NULL, ",");
        index++;
    }
    
    // Debug print to verify parsing
    Serial.print("Parsed ratios: ");
    for (int i = 0; i < index; i++) {
        Serial.print(ratios[i]);
        Serial.print(" ");
    }
    Serial.println();
    
    // Call dispense with the parsed ratios
    dispense(ratios);
    Serial.println("ack");
}

    



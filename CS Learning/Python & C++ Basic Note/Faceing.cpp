#include <iostream>
#include <string>
using namespace std;

class Robot {
private:
    int energy = 100;
    string name;

protected:
    string getName() const {
        return name;
    }

    int getEnergy() const {
        return energy;
    }

    void useEnergy(int amount) {
        energy -= amount;

        if (energy < 0) {
            energy = 0;
        }
    }

public:
    Robot(string robotName) : name(robotName) {
        cout << "Robot " << name << " created with energy: "
             << energy << endl;
    }

    virtual ~Robot() {
        cout << "Robot " << name << " destroyed." << endl;
    }

    void sayHello() {
        cout << "Hello, " << name << endl;
    }

    void charge(int amount) {
        if (amount >= 0) {
            energy += amount;
            cout << name << "'s energy is now "
                 << energy << endl;
        }
    }

    virtual void move() {
        cout << name << " is moving. Energy: "
             << energy << endl;

        useEnergy(10);
    }

    void stop() {
        cout << name << " has stopped. Energy: "
             << energy << endl;
    }
};

class SoccerRobot : public Robot {
public:
    SoccerRobot(string robotName) : Robot(robotName) {}

    void kick() {
        cout << getName() << " is kicking the ball!" << endl;
    }

    void move() override {
        cout << getName() << " is moving on the field. Energy: "
             << getEnergy() << endl;

        useEnergy(15);
    }
};

class RescueRobot : public Robot {
public:
    RescueRobot(string robotName) : Robot(robotName) {}

    void rescue() {
        cout << getName()
             << " is performing a rescue operation!" << endl;
    }

    void move() override {
        cout << getName()
             << " is moving to the rescue site. Energy: "
             << getEnergy() << endl;

        useEnergy(20);
    }
};

int main() {
    SoccerRobot soccerBot("SoccerBot");
    RescueRobot rescueBot("RescueBot");

    soccerBot.sayHello();
    soccerBot.move();
    soccerBot.kick();
    soccerBot.charge(20);
    soccerBot.stop();

    cout << endl;

    rescueBot.sayHello();
    rescueBot.move();
    rescueBot.rescue();
    rescueBot.charge(30);
    rescueBot.stop();

    return 0;
}
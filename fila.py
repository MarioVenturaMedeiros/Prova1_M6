from collections import deque
import rclpy
from rclpy.node import Node
from turtlesim.srv import Spawn, Kill
from geometry_msgs.msg import Twist
import time

# Criação de um deque vazio
dq = deque()

# Adicionando elementos no final
print(f"Deque após append: {dq}")

# Adicionando elementos no início
dq.appendleft('X')
dq.appendleft('Y')
print(f"Deque após appendleft: {dq}")

# Removendo elementos do final
dq.pop()
print(f"Deque após pop: {dq}")

# Removendo elementos do início
dq.popleft()
print(f"Deque após popleft: {dq}")

# Rotacionando o deque
dq.rotate(1)
print(f"Deque após rotate(1): {dq}")

# Verificando o comprimento do deque
print(f"Tamanho do deque: {len(dq)}")

class Tartaruguinha(Node):
    def __init__(self, start_x, start_y, start_z, period, turtle_name):
        super().__init__('tartaruguinha_eu_escolho_voce')
        self.turtle_name = turtle_name
        self.spawn = self.create_client(Spawn, 'spawn')
        self.kill = self.create_client(Kill, 'kill')
        self.move = self.create_publisher(Twist, f'{self.turtle_name}/cmd_vel', 10)
        self.start_x = float(start_x)
        self.start_y = float(start_y)
        self.start_z = float(start_z)
        self.period = int(period)
        self.spawn_turtle()

    def spawn_turtle(self):
        self.get_logger().info(f"Spawning turtle: {self.turtle_name} at x={self.start_x}")
        spawn = Spawn.Request()
        spawn.x = 5.0
        spawn.y = 5.0
        spawn.theta = 0.0
        spawn.name = self.turtle_name
        future = self.spawn.call_async(spawn)
        rclpy.spin_until_future_complete(self, future)

    def movimenta(self):
        twist = Twist()
        print(dq[0])
        primeiro = float(dq[0][0])
        segundo = float(dq[0][1])
        terceiro = float(dq[0][2])
        print(primeiro, segundo, terceiro)
        moves = [
            (primeiro, segundo, terceiro)
        ]
        for linear_x, angular_z, duration in moves:
            twist.linear.x = linear_x
            twist.angular.z = angular_z
            for _ in range(duration):
                print(twist)
                self.move.publish(twist)
                time.sleep(self.period)
        self.stop_and_kill_turtle()

    def stop_and_kill_turtle(self):
        # Stop and kill the turtle
        twist = Twist()
        twist.linear.x = 0.0
        twist.angular.z = 0.0
        self.move.publish(twist)
        kill = Kill.Request()
        kill.name = self.turtle_name
        self.kill.call_async(kill)
        self.get_logger().info(f'Seu trabalho aqui acabou, {self.turtle_name}')

def main(args=None):
    rclpy.init(args=args)
    while True:
        try:
            vx = float(input("Escreva a velocidade em X da tartaruguinha: "))
            print(vx + 1)
            vy = float(input("Escreva a velocidade em Y da tartaruguinha: "))
            vt = float(input("Escreva a velocidade angular da tartaruguinha: "))
            period = int(input("Escreva o período de ativação da tartaruguinha: "))
        except:
            print("Seu formato de mensagem não foi o adequado.")
            break
        dq.append([vx, vy, vt])
        print(f"Deque após append: {dq}")
        turtle = Tartaruguinha(vx, vy, vt, period, 'm1_turtle')
        turtle.movimenta()
    
        rclpy.shutdown()

if __name__ == '__main__':
    main()

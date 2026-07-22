import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Joy
from rcl_interfaces.srv import SetParameters
from rcl_interfaces.msg import Parameter, ParameterValue, ParameterType

BTN_X = 0        # sube velocidad
BTN_CIRCLE = 1   # baja velocidad
BTN_STOP = 3     # <-- confirmar índice real de Y con ros2 topic echo /joy

STEP = 0.1
MIN_SCALE = 0.1
MAX_SCALE = 1.0

INITIAL_LINEAR = 0.5   # igual al scale_linear del yaml
INITIAL_ANGULAR = 1.0  # igual al scale_angular del yaml


class SpeedManager(Node):
    def __init__(self):
        super().__init__('speed_manager')
        self.prev_buttons = []

        self.linear_scale = INITIAL_LINEAR
        self.angular_scale = INITIAL_ANGULAR
        self.stopped = False

        self.sub = self.create_subscription(Joy, '/joy', self.joy_cb, 10)

        self.set_param_cli = self.create_client(
            SetParameters, '/teleop_twist_joy_node/set_parameters')

        self.get_logger().info('Esperando servicio set_parameters de teleop_twist_joy_node...')
        while not self.set_param_cli.wait_for_service(timeout_sec=2.0):
            self.get_logger().info('Sigo esperando...')

        self.get_logger().info(
            f'Speed manager listo. Lineal: {self.linear_scale}, Angular: {self.angular_scale}')

    def joy_cb(self, msg: Joy):
        if not self.prev_buttons or len(self.prev_buttons) != len(msg.buttons):
            self.prev_buttons = list(msg.buttons)
            return

        x_pressed = msg.buttons[BTN_X] == 1 and self.prev_buttons[BTN_X] == 0
        o_pressed = msg.buttons[BTN_CIRCLE] == 1 and self.prev_buttons[BTN_CIRCLE] == 0
        stop_pressed = msg.buttons[BTN_STOP] == 1 and self.prev_buttons[BTN_STOP] == 0

        if stop_pressed:
            # Frena TODO: lineal y angular en 0.0.
            # No hay reanudación automática al re-tocar Y.
            self.stopped = True
            self.get_logger().warn('FRENO DE EMERGENCIA: velocidad en 0.0')
            self.push_params(0.0, 0.0)

        elif x_pressed:
            # Al subir velocidad, si estaba frenado, sale del estado de freno
            # y retoma desde el mínimo (no desde donde estaba antes de frenar).
            if self.stopped:
                self.stopped = False
                self.linear_scale = MIN_SCALE
                self.angular_scale = INITIAL_ANGULAR
            else:
                self.linear_scale = min(MAX_SCALE, round(self.linear_scale + STEP, 2))

            self.get_logger().info(f'Nueva velocidad lineal: {self.linear_scale}')
            self.push_params(self.linear_scale, self.angular_scale)

        elif o_pressed and not self.stopped:
            self.linear_scale = max(MIN_SCALE, round(self.linear_scale - STEP, 2))
            self.get_logger().info(f'Nueva velocidad lineal: {self.linear_scale}')
            self.push_params(self.linear_scale, self.angular_scale)

        self.prev_buttons = list(msg.buttons)

    def push_params(self, linear_value, angular_value):
        req = SetParameters.Request()

        for name, value in [
            ('scale_linear.x', linear_value),
            ('scale_linear.y', linear_value),
            ('scale_angular.yaw', angular_value),
        ]:
            p = Parameter()
            p.name = name
            p.value = ParameterValue(
                type=ParameterType.PARAMETER_DOUBLE,
                double_value=value)
            req.parameters.append(p)

        self.set_param_cli.call_async(req)


def main():
    rclpy.init()
    node = SpeedManager()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
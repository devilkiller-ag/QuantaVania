import pygame
from qiskit import QuantumRegister, QuantumCircuit
import numpy as np

from pygame.image import load as loadImage
from settings import *


class QuantumCircuitGridBackground(pygame.sprite.Sprite):
    def __init__(self, qc_grid_model):
        super().__init__()
        self.qc_grid_model = qc_grid_model
        self.width = QUANTUM_CIRCUIT_TILE_SIZE * (self.qc_grid_model.max_columns + 2)
        self.height = QUANTUM_CIRCUIT_TILE_SIZE * (self.qc_grid_model.max_wires + 1)
        
        # BACKGROUND SURFACE
        self.qc_bg_surface = pygame.Surface((self.width, self.height))
        self.qc_bg_surface.fill(QUANTUM_CIRCUIT_COLOR_COLOR)
        self.rect = self.qc_bg_surface.get_rect()
        self.rect.inflate_ip(-WIRE_LINE_WIDTH, -WIRE_LINE_WIDTH)

    def draw_qubit_wires(self):
        for wire in range(self.qc_grid_model.num_qubits):
            x_start = QUANTUM_CIRCUIT_TILE_SIZE * 0.5
            x_end = self.width - (QUANTUM_CIRCUIT_TILE_SIZE * 0.5)
            y = (wire + 1) * QUANTUM_CIRCUIT_TILE_SIZE 
            pygame.draw.line(
                self.qc_bg_surface, 
                QUANTUM_CIRCUIT_WIRE_COLOR, 
                (x_start, y), 
                (x_end, y),
                WIRE_LINE_WIDTH
            )

    def run(self):
        # Drawing
        pygame.draw.rect(self.qc_bg_surface, QUANTUM_CIRCUIT_WIRE_COLOR, self.rect, WIRE_LINE_WIDTH)
        self.draw_qubit_wires()

class QuantumCircuitGridMarker(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.qc_bg_surface = loadImage("graphics/circuit_gates/circuit-grid-cursor.png").convert_alpha()
        self.rect = self.qc_bg_surface.get_rect()

class QuantumCircuitGridNode:
    def __init__(self, gate_type, rotation_angle = 0.0, first_ctrl = -1, second_ctrl = -1, swap = -1):
        self.gate_type = gate_type # What Gate is at this node
        self.rotation_angle = rotation_angle # If radian != 0 then this node have a U(theta) gate; Ex:- RX, RY, RZ
        self.first_ctrl = first_ctrl # If first_ctrl > 0; then this node is a controlled gate with one control node
        self.second_ctrl = second_ctrl # If second_ctrl > 0; then this node is a controlled gate with two control nodes
        self.swap = swap # If swap != -1 then this node have a swap gate

    def __str__(self):
        string = "Type: " + str(self.gate_type)
        string += ", rotation_angle: " + str(self.rotation_angle) if self.rotation_angle != 0 else ""
        string += ", ctrl_a: " + str(self.first_ctrl) if self.first_ctrl != -1 else ""
        string += ", ctrl_b: " + str(self.second_ctrl) if self.second_ctrl != -1 else ""
        return string

class QuantumCircuitGridGate(pygame.sprite.Sprite):
    def __init__(self, qc_grid_model, wire, column):
        super().__init__()
        self.qc_grid_model = qc_grid_model
        
        # Gate Position
        self.wire = wire
        self.column = column
    
    def import_gate(gate_name, colorkey = None):
        gate_image_folder = "graphics/quantum_gates"
        gate_image = loadImage(f"{gate_image_folder}/{gate_name}")
        if colorkey is not None:
            if colorkey == -1:
                colorkey = gate_image.get_at((0,0))
            gate_image.set_colorkey(colorkey)
        return gate_image, gate_image.get_rect()

    def load_gate(self):
        gate = self.qc_grid_model.get_node_gate(self.wire, self.column)
        
        if gate == GATES['IDEN']:
            self.gate_surface, self.gate_rect = self.import_gate("iden_gate.png", -1)    
        
        elif gate == GATES['X']:
            node = self.qc_grid_model.get_node(self.wire, self.column)
            # Check if this is a CNOT Gate
            if node.first_ctrl >= 0 or node.second_ctrl >= 0:
                if self.wire > max(node.ctrl_a, node.ctrl_b): # If target wire is below control wire
                    self.gate_surface, self.gate_rect = self.import_gate("not_gate_below_ctrl.png", -1)
                else: # If target wire is above control wire
                    self.gate_surface, self.gate_rect = self.import_gate("not_gate_above_ctrl.png", -1)
            elif node.rotation_angle != 0: # Else If this is a RX Gate
                self.gate_surface, self.gate_rect = self.import_gate("rx_gate.png", -1)
                # Draw the value of theta as an arc of a circle 
                pygame.draw.arc(self.gate_surface, QUANTUM_GATE_PHASE_COLOR, self.gate_rect, 0, node.rotation_angle % (2 * np.pi), 4)
            else: # Else if this is a normal X Gate
                self.gate_surface, self.gate_rect = self.import_gate("x_gate.png", -1)
        
        elif gate == GATES['Y']:
            node = self.qc_grid_model.get_node(self.wire, self.column)
            # Check if this is a RY Gate
            if node.rotation_angle != 0:
                self.gate_surface, self.gate_rect = self.import_gate("ry_gate.png", -1)
                # Draw the value of theta as an arc of a circle 
                pygame.draw.arc(self.gate_surface, QUANTUM_GATE_PHASE_COLOR, self.gate_rect, 0, node.rotation_angle % (2 * np.pi), 4)
            else: # Else if this is a normal Y Gate
                self.gate_surface, self.gate_rect = self.import_gate("y_gate.png", -1)
        
        elif gate == GATES['Z']:
            node = self.qc_grid_model.get_node(self.wire, self.column)
            # Check if this is a RY Gate
            if node.rotation_angle != 0:
                self.gate_surface, self.gate_rect = self.import_gate("rz_gate.png", -1)
                # Draw the value of theta as an arc of a circle 
                pygame.draw.arc(self.gate_surface, QUANTUM_GATE_PHASE_COLOR, self.gate_rect, 0, node.rotation_angle % (2 * np.pi), 4)
            else: # Else if this is a normal Y Gate
                self.gate_surface, self.gate_rect = self.import_gate("z_gate.png", -1)
        
        elif gate == GATES['S']:
            self.gate_surface, self.gate_rect = self.import_gate("s_gate.png", -1)
        
        elif gate == GATES['SDG']:
            self.gate_surface, self.gate_rect = self.import_gate("sdg_gate.png", -1)
        
        elif gate == GATES['T']:
            self.gate_surface, self.gate_rect = self.import_gate("t_gate.png", -1)
        
        elif gate == GATES['TDG']:
            self.gate_surface, self.gate_rect = self.import_gate("tdg_gate.png", -1)

        elif gate == GATES['H']:
            self.gate_surface, self.gate_rect = self.import_gate("h_gate.png", -1)
        
        elif gate == GATES['SWAP']:
            self.gate_surface, self.gate_rect = self.import_gate("swap_gate.png", -1)
        
        elif gate == GATES['CTRL']:
            # Check if the target wire is above the control wire
            if self.wire > self.qc_grid_model.get_wire_for_control_node_at(self.wire, self.column):
                self.gate_surface, self.gate_rect = self.import_gate("ctrl_gate_bottom_wire.png", -1)
            else: # if the target wire is above the control wire
                self.gate_surface, self.gate_rect = self.import_gate("ctrl_gate_top_wire.png", -1)
        
        elif gate == GATES['CTRL_LINE']:
            self.gate_surface, self.gate_rect = self.import_gate("ctrl_line_gate.png", -1)
        
        else: # If the node is empty
            # Draw a transparent block, i.e., empty gate/node
            self.gate_surface = pygame.Surface([GATE_TILE_WIDTH, GATE_TILE_HIEGHT])
            self.gate_surface.set_alpha(0)
            self.rect = self.image.get_rect()
        
        self.gate_surface.convert()

    def run(self):
        self.load_gate()

class QuantumCircuitGridModel():
    def __init__(self, num_qubits, num_columns):
        self.num_qubits = num_qubits
        self.num_columns = num_columns
        self.nodes = np.zeros(
            (self.circuit_grid_model.max_wires, self.circuit_grid_model.max_columns),
            dtype=QuantumCircuitGridNode
        )
    
    def __str__(self):
        string = "CircuitGridModel:\n"
        for wire in range(self.num_qubits):
            row_values = [str(self.get_gate_at_node(wire, column)) for column in range(self.num_columns)]
            string += ", ".join(row_values) + "\n"
        return string

    def set_node(self, wire, column, qc_grid_node):
        self.nodes[wire][column] = QuantumCircuitGrid(
            qc_grid_node.gate_type,
            qc_grid_node.rotation_angle,
            qc_grid_node.first_ctrl,
            qc_grid_node.second_ctrl,
            qc_grid_node.swap
        )
    
    def get_node(self, wire, column):
        return self.nodes[wire][column]

    def get_gate_at_node(self, wire, column):
        node = self.node[wire][column]
        
        if node and node.gate_type != GATES['EMPTY']: # If the node is already occupied
            return node.gate_type # Return the gate occupying the node
        
        column_nodes = self.nodes[:, column]
        for index, other_node in enumerate(column_nodes):
            if index != wire and other_node:
                # Check if the other_node is a control node
                if other_node.first_ctrl == wire or other_node.second_ctrl == wire:
                    return GATES['CTRL']
                # Or if it is a swap node
                elif other_node.swap == wire:
                    return GATES['SWAP']
        
        # If no gate is present at the node return 'EMPTY'
        return GATES['EMPTY']

    def get_wire_for_control_node_at(self, control_wire, column):
        control_wire = -1
        column_nodes = self.nodes[:, column]

        for index in range(self.num_qubits):
            if index != control_wire:
                other_node = column_nodes[index]
                if other_node:
                    if (other_node.first_ctrl == control_wire or other_node.second_ctrl == control_wire):
                        control_wire = index
                        print("Found ", self.get_gate_at_node(control_wire, column), " on wire ", control_wire)
        
        return control_wire

    def compute_quantum_circuit(self):
        """Create and Compute Quantum Circuit from Quantum Circuit Grid"""
        qr = QuantumRegister(self.num_qubits, "q")
        qc = QuantumCircuit(qr)

        for column in range(self.num_columns):
            for wire in range(self.num_qubits):
                node = self.nodes[wire][column]
                
                if node:
                    if node.gate_type == GATES['IDENTITY']:
                        qc.i(qr[wire])

                    elif node.gate_type == GATES['X']:
                        if node.rotation_angle == 0: # Node have a normal X Gate
                            if node.first_ctrl != -1: # If first control is active
                                if node.second_ctrl != -1: # If second control is also active then node have a Toffoli Gate
                                    qc.ccx(qr[node.frist_ctrl], qr[node.second_ctrl], qr[wire])
                                else: # Node have a Controlled X Gate
                                    qc.cx(qr[node.frist_ctrl], qr[wire])
                            else: # If no control is active then the node have a Pauli X Gate
                                qc.x(qr[wire])
                        else: # If angle is not zero then it is a RX Gate
                            qc.rx(node.rotation_angle, qr[wire])
                    
                    



class QuantumCircuitGrid(pygame.sprite.RenderPlain):
    def __init__(self, position):
        super().__init__()
        
        ## State
        self.position = position
        self.current_wire = 0
        self.current_column = 0
        
        self.qc_grid_model = QuantumCircuitGridModel()
        self.circuit_grid_background = QuantumCircuitGridBackground()
        self.circuit_grid_background = QuantumCircuitGridMarker()

        self.gate_tiles = np.zeros(
            (self.circuit_grid_model.max_wires, self.circuit_grid_model.max_columns),
            dtype=QuantumCircuitGridGate
        )
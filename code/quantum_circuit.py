import pygame
import qiskit
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

class QuantumCircuitGridGate(pygame.sprite.Sprite):
    def __init__(self, qc_grid_model, wire, column):
        super().__init__()
        self.qc_grid_model = qc_grid_model

class QuantumCircuitGridModel():
    def __init__(self, num_qubits, num_columns):
        self.num_qubits = num_qubits
        self.num_columns = num_columns

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
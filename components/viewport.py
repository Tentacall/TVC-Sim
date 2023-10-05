from PySide6.QtGui import (QMatrix4x4, QOpenGLContext, QSurfaceFormat, QWindow)
from PySide6.QtOpenGL import (QOpenGLBuffer, QOpenGLShader,
                              QOpenGLShaderProgram, QOpenGLVertexArrayObject)
from PySide6.QtCore import Slot, Qt

class RenderWindow(QWindow):
    def __init__(self, fmt):
        super().__init__()
        self.setSurfaceType(QWindow.OpenGLSurface)
        self.setFormat(fmt)
        self.context = QOpenGLContext(self)
        self.context.setFormat(self.requestedFormat())
        if not self.context.create():
            raise Exception("Unable to create GL context")
        
        self.program = None

    def init_gl(self):
        self.program = QOpenGLShaderProgram(self)
        self.vao = QOpenGLVertexArrayObject()
        self.vbo = QOpenGLBuffer()

        fmt = self.context.format()
        use_new_style_shader = fmt.profile() == QSurfaceFormat.CoreProfile


    def render():
        pass
    
    @Slot()
    def slot_timer(self):
        self.render()

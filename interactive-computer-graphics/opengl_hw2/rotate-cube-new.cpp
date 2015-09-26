
#include "Angel-yjc.h"
#pragma comment(lib, "glew32.lib")
#include <fstream>
#include <string>
#include <math.h>
using namespace std;

typedef Angel::vec3  color3;
typedef Angel::vec3  point3;

GLuint Angel::InitShader(const char* vShaderFile, const char* fShaderFile);

GLuint program;       /* shader program object id */
GLuint cube_buffer;   /* vertex buffer object id for cube */
GLuint floor_buffer;  /* vertex buffer object id for floor */
GLuint line_buffer;

GLuint quadrilateral_buffer; //vertex buffer object id for quadrilateral
GLuint X_axis_buffer;		 //vertex buffer object id for X_axis
GLuint Y_axis_buffer;		 //vertex buffer object id for Y_axis
GLuint Z_axis_buffer;		 //vertex buffer object id for Z_axis
GLuint sphere_buffer;		 //vertex buffer object id for sphere

// Projection transformation parameters
GLfloat  fovy = 45.0;  // Field-of-view in Y direction angle (in degrees)
GLfloat  aspect;       // Viewport aspect ratio
GLfloat  zNear = 0.5, zFar = 13.0;
GLfloat radius;

GLfloat angle = 0.0; // rotation angle in degrees
vec4 init_eye(7.0, 3.0, -10.0, 1.0); // initial viewer position
vec4 eye = init_eye;               // current viewer position

int animationFlag = 1; // 1: animation; 0: non-animation. Toggled by key 'a' or 'A'

int cubeFlag = 1;   // 1: solid cube; 0: wireframe cube. Toggled by key 'c' or 'C'
int floorFlag = 1;  // 1: solid floor; 0: wireframe floor. Toggled by key 'f' or 'F'
int sphereFlag = 1;

const int cube_NumVertices = 36; //(6 faces)*(2 triangles/face)*(3 vertices/triangle)

point3 cube_points[100];
color3 cube_colors[100];

point3 track[] = { point3(3.0, 1.0, 5.0), point3(-2.0, 1.0, -2.5), point3(2.0, 1.0, -4.0) };
int currentSegment = 0, totalSegments = 3;
GLfloat theta = 0.0, delta = 0.06;//moving and rotation speed
point3 centerPos = track[currentSegment];
point3*vectors;
point3*rotationAxis;
#define PI 3.14159265358979323846
#define sqrt3f(x,y,z) sqrt(x*x+y*y+z*z)
float distanceAt(point3 p1, point3 p2);
mat4 acc_matrix = Angel::identity();
bool begin1 = false, rolling = false;

const int floor_NumVertices = 6; //(1 face)*(2 triangles/face)*(3 vertices/triangle)
point3 floor_points[floor_NumVertices]; // positions for all vertices
color3 floor_colors[floor_NumVertices]; // colors for all vertices

point3 vertices[4] = {
    point3( 5, 0,  8),
    point3( 5, 0,  -4),
    point3(  -5,  0,  -4),
	point3(  -5,  0,  8),
};
// RGBA colors
color3 vertex_colors[8] = {
    color3( 0.0, 0.0, 0.0),  // black
    color3( 1.0, 0.0, 0.0),  // red
    color3( 1.0, 0.84, 0.0),  //golden_yellow
    color3( 0.0, 1.0, 0.0),  // green
    color3( 0.0, 0.0, 1.0),  // blue
    color3( 1.0, 0.0, 1.0),  // magenta
    color3( 1.0, 1.0, 1.0),  // white
    color3( 0.0, 1.0, 1.0)   // cyan
};

point3 line_points[9];
color3 line_colors[9];

point3 *sphereData;
color3 *sphere_color;
int sphere_NumVertices;

int col;//Numbers of triangles
//----------------------------------------------------------------------------
void xyz_line()
{
	line_colors[0]=vertex_colors[1];line_points[0]=point3(0,0,0);
	line_colors[1]=vertex_colors[1];line_points[1]=point3(10,0,0);
	line_colors[2]=vertex_colors[1];line_points[2]=point3(20,0,0);

	line_colors[3]=vertex_colors[5];line_points[3]=point3(0,0,0);
	line_colors[4]=vertex_colors[5];line_points[4]=point3(0,10,0);
	line_colors[5]=vertex_colors[5];line_points[5]=point3(0,20,0);

	line_colors[6]=vertex_colors[4];line_points[6]=point3(0,0,0);
	line_colors[7]=vertex_colors[4];line_points[7]=point3(0,0,10);
	line_colors[8]=vertex_colors[4];line_points[8]=point3(0,0,20);
}
//----------------------------------------------------------------------------
int Index = 0; // YJC: This must be a global variable since quad() is called
//      multiple times and Index should then go up to 36 for
//      the 36 vertices and colors
int Index1 = 0;

//----------------------------------------------------------------------------
//File in
void readFiles()
{
	ifstream fp;
	char* filename=new char[100];

	int points;
	float temp[3];

	int count = 0;
	cout<<"Enter the filename. [sphere.8 or sphere.128],press ENTER use sphere.128" << endl;

	cin.getline(filename,100);
	if(strlen(filename) == 0){
		filename = "sphere.128";
	}
	fp.open(filename);
	if (!fp) {
		cerr << "Couldn't open " << filename << " !" << endl;
		exit(0);
	}
	fp >> col;
	cout << col << endl;
	sphereData = new point3[col * 3];
	sphere_color = new point3[col * 3];
	for (int i = 0; i < col; i++) {
		fp >> points;
		for (int j = 0; j < points; j++) {
			for (int k = 0; k < 3; k++) {	
				fp >> temp[k];

			}
			point3 tmp( temp[0], temp[1], temp[2]);
			sphereData[count++] = tmp;
			//	cout << sphereData[count - 1] << endl;
		}
	}
	sphere_NumVertices = col * 3;
	fp.close();
}

void colorsphere()
{
	for (int i = 0; i < col * 3; i++) {
		sphere_color[i] = color3(1.0, 0.84, 0.0);
	}

}
//-------------------------------
// generate 2 triangles: 6 vertices and 6 colors
void floor()
{
	floor_colors[0] = vertex_colors[3]; floor_points[0] = vertices[0];
    floor_colors[1] = vertex_colors[3]; floor_points[1] = vertices[1];
    floor_colors[2] = vertex_colors[3]; floor_points[2] = vertices[2];
    floor_colors[3] = vertex_colors[3]; floor_points[3] = vertices[0];
	floor_colors[4] = vertex_colors[3]; floor_points[4] = vertices[3];
    floor_colors[5] = vertex_colors[3]; floor_points[5] = vertices[2];
}
//---------------------------------------------------------------------------
//calculate the Direction
point3 calculateDirection(point3 from, point3 to){
	point3 v;
	v.x = to.x - from.x;
	v.y = to.y - from.y;
	v.z = to.z - from.z;

	//convert v to unit-length
	float d = sqrt3f(v.x, v.y, v.z);
	v.x = v.x / d;
	v.y = v.y / d;
	v.z = v.z / d;

	return v;
}
point3 crossProduct(point3 u, point3 v){
	point3 n;
	n.x = u.y*v.z - u.z*v.y;
	n.y = u.z*v.x - u.x*v.z;
	n.z = u.x*v.y - u.y*v.x;
	return n;
}
//----------------------------------------------------------------------------
// OpenGL initialization
void init()
{
	//colorcube();
	radius = 1;
	colorsphere();

	//calculate the rolling directions
	totalSegments = sizeof(track) / sizeof(point3);
	vectors = new point3[totalSegments];
	rotationAxis = new point3[totalSegments];
	for (int i = 0; i<totalSegments - 1; i++){
		vectors[i] = calculateDirection(track[i], track[i + 1]);
	}
	//and the last point to the first one
	vectors[totalSegments - 1] = calculateDirection(track[totalSegments - 1], track[0]);

	//calculate the rotating axis vectors
	point3 y_axis(0, 1, 0 );
	for (int i = 0; i<totalSegments; i++){
		rotationAxis[i] = crossProduct(y_axis, vectors[i]);
	}
	// Create and initialize a vertex buffer object for cube, to be used in display()
	glGenBuffers(1, &cube_buffer);
	glBindBuffer(GL_ARRAY_BUFFER, cube_buffer);

	glBufferData(GL_ARRAY_BUFFER, sizeof(point3) * cube_NumVertices + sizeof(color3) * cube_NumVertices,
		NULL, GL_STATIC_DRAW);
	glBufferSubData(GL_ARRAY_BUFFER, 0, sizeof(point3) * cube_NumVertices, cube_points);
	glBufferSubData(GL_ARRAY_BUFFER, sizeof(point3) * cube_NumVertices, sizeof(color3) * cube_NumVertices,
		cube_colors);

	floor();

	// Create and initialize a vertex buffer object for floor, to be used in display()

	glGenBuffers(1, &floor_buffer);
	glBindBuffer(GL_ARRAY_BUFFER, floor_buffer);
	glBufferData(GL_ARRAY_BUFFER, sizeof(floor_points) + sizeof(floor_colors),
		NULL, GL_STATIC_DRAW);
	glBufferSubData(GL_ARRAY_BUFFER, 0, sizeof(floor_points), floor_points);
	glBufferSubData(GL_ARRAY_BUFFER, sizeof(floor_points), sizeof(floor_colors),
		floor_colors);

	xyz_line();
	glGenBuffers(1, &line_buffer);
    glBindBuffer(GL_ARRAY_BUFFER, line_buffer);
    glBufferData(GL_ARRAY_BUFFER, sizeof(line_points) + sizeof(line_colors),
		 NULL, GL_STATIC_DRAW);
    glBufferSubData(GL_ARRAY_BUFFER, 0, sizeof(line_points), line_points);
    glBufferSubData(GL_ARRAY_BUFFER, sizeof(line_points), sizeof(line_colors),
                    line_colors);


	// create and initialize a vertex buffer object for sphere.
	glGenBuffers(1, &sphere_buffer);
	glBindBuffer(GL_ARRAY_BUFFER, sphere_buffer);
	glBufferData(GL_ARRAY_BUFFER, 3 * col * sizeof(point3) + 3 * col * sizeof(color3),
		NULL, GL_STATIC_DRAW);
	glBufferSubData(GL_ARRAY_BUFFER, 0, 3 * col * sizeof(point3), sphereData);
	glBufferSubData(GL_ARRAY_BUFFER, 3 * col * sizeof(point3), 3 * col * sizeof(color3),
		sphere_color);

	// Load shaders and create a shader program (to be used in display())
	program = InitShader("vshader42.glsl", "fshader42.glsl");

	glEnable(GL_DEPTH_TEST);
	glClearColor(0.0, 0.0, 0.0, 1.0);
	glLineWidth(2.0);
}
//----------------------------------------------------------------------------
// drawObj(buffer, num_vertices):
//   draw the object that is associated with the vertex buffer object "buffer"
//   and has "num_vertices" vertices.
//
void drawObj(GLuint buffer, int num_vertices)
{
	//--- Activate the vertex buffer object to be drawn ---//
	glBindBuffer(GL_ARRAY_BUFFER, buffer);

	/*----- Set up vertex attribute arrays for each vertex attribute -----*/
	GLuint vPosition = glGetAttribLocation(program, "vPosition");
	glEnableVertexAttribArray(vPosition);
	glVertexAttribPointer(vPosition, 3, GL_FLOAT, GL_FALSE, 0,
		BUFFER_OFFSET(0));

	GLuint vColor = glGetAttribLocation(program, "vColor");
	glEnableVertexAttribArray(vColor);
	glVertexAttribPointer(vColor, 3, GL_FLOAT, GL_FALSE, 0,
		BUFFER_OFFSET(sizeof(point3) * num_vertices));
	// the offset is the (total) size of the previous vertex attribute array(s)

	/* Draw a sequence of geometric objs (triangles) from the vertex buffer
	(using the attributes specified in each enabled vertex attribute array) */
	glDrawArrays(GL_TRIANGLES, 0, num_vertices);

	/*--- Disable each vertex attribute array being enabled ---*/
	glDisableVertexAttribArray(vPosition);
	glDisableVertexAttribArray(vColor);
}
//----------------------------------------------------------------------------
void display(void)
{
	GLuint  model_view;  // model-view matrix uniform shader variable location
	GLuint  projection;  // projection matrix uniform shader variable location

	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);

	glUseProgram(program); // Use the shader program

	model_view = glGetUniformLocation(program, "model_view");
	projection = glGetUniformLocation(program, "projection");
	glClearColor(0.529, 0.807, 0.92, 0.0);
	/*---  Set up and pass on Projection matrix to the shader ---*/
	mat4  p = Perspective(fovy, aspect, zNear, zFar);
	glUniformMatrix4fv(projection, 1, GL_TRUE, p); // GL_TRUE: matrix is row-major

	/*---  Set up and pass on Model-View matrix to the shader ---*/
	// eye is a global variable of vec4 set to init_eye and updated by keyboard()
	//at=eye+VPN
	vec4    at(0.0, 0.0, 0.0, 1.0);
	vec4    up(0.0, 1.0, 0.0, 0.0);
	//  eye = Translate(0.0, 0.0, 0.0)*eye;
	mat4  mv = LookAt(eye, at, up);
	
	glUniformMatrix4fv(model_view, 1, GL_TRUE, mv); // GL_TRUE: matrix is row-major
	if (floorFlag == 1) // Filled floor
		glPolygonMode(GL_FRONT_AND_BACK, GL_FILL);
	else              // Wireframe floor
		glPolygonMode(GL_FRONT_AND_BACK, GL_LINE);
	drawObj(floor_buffer, floor_NumVertices);  // draw the floor
	

	glUniformMatrix4fv(model_view, 1, GL_TRUE, mv); // GL_TRUE: matrix is row-major           
    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE);
	drawObj(line_buffer,9); //draw xyz line
	
	//start to draw the sphere
	//mv = Translate(-6.5, 1.0, -4.0) * LookAt(eye, at, up)*Scale(1.2,1.2,1.2);
	
	//at = centerPos;
	//cout << at << endl;
	acc_matrix =  Rotate(delta, rotationAxis[currentSegment].x, rotationAxis[currentSegment].y, rotationAxis[currentSegment].z)*acc_matrix;
	mv = LookAt(eye, at, up)*Translate(centerPos.x, centerPos.y, centerPos.z) *acc_matrix;

	glUniformMatrix4fv(model_view, 1, GL_TRUE, mv);
	glPolygonMode(GL_FRONT_AND_BACK, GL_LINE);
	drawObj(sphere_buffer, sphere_NumVertices);

	glutSwapBuffers();
}
//---------------------------------------------------------------------------
/* Compute distance between two points */
float distanceAt(point3 p1, point3 p2){
	float dx = p1.x - p2.x;
	float dy = p1.y - p2.y;
	float dz = p1.z - p2.z;
	return sqrt3f(dx, dy, dz);
}

int nextModel(){
	int next = currentSegment + 1;
	return (next == totalSegments) ? 0 : next;
}
/* distance between current position and next point is greater than one between current track point and the next point*/
bool isTrespass(){
	int next = nextModel();
	point3 from = track[currentSegment];
	point3 to = track[next];
	float d1 = distanceAt(centerPos, from);
	float d2 = distanceAt(to, from);

	return d1 > d2;
}

//---------------------------------------------------------------------------
void idle(void)
{
	//angle += 0.2;
	// angle += 1.0;    //YJC: change this value to adjust the cube rotation speed.
	//rotate by constant speed
	theta += delta;
	if (theta > 360.0)
		theta -= 360.0;
	//translate on direction 
	float offset = (radius*delta*PI) / 180;
	centerPos.x = centerPos.x + vectors[currentSegment].x*offset;
	centerPos.y = centerPos.y + vectors[currentSegment].y*offset;
	centerPos.z = centerPos.z + vectors[currentSegment].z*offset;
	if (isTrespass()){
		currentSegment = nextModel();
		centerPos = track[currentSegment];
	}

	//display
	glutPostRedisplay();
}
//----------------------------------------------------------------------------

void keyboard(unsigned char key, int x, int y)
{
	switch (key) {
	case 033: // Escape Key
	case 'q': case 'Q':
		exit(EXIT_SUCCESS);
		break;
	case 'b':case'B'://start Rolling
		begin1 = true;
		glutIdleFunc(idle);
		break;
	case 'X': eye[0] += 1.0; break;
	case 'x': eye[0] -= 1.0; break;
	case 'Y': eye[1] += 1.0; break;
	case 'y': eye[1] -= 1.0; break;
	case 'Z': eye[2] += 1.0; break;
	case 'z': eye[2] -= 1.0; break;

	case 'a': case 'A': // Toggle between animation and non-animation
		animationFlag = 1 - animationFlag;
		if (animationFlag == 1) glutIdleFunc(idle);
		else                    glutIdleFunc(NULL);
		break;

	case 'c': case 'C': // Toggle between filled and wireframe cube
		cubeFlag = 1 - cubeFlag;
		break;

	case 'f': case 'F': // Toggle between filled and wireframe floor
		floorFlag = 1 - floorFlag;
		break;

	case ' ':  // reset to initial viewer/eye position
		eye = init_eye;
		break;
	}
	glutPostRedisplay();
}
//----------------------------------------------------------------------------
void mouse(int button, int state, int x, int y){
	if (button == GLUT_RIGHT_BUTTON && state == GLUT_UP && begin1){
		rolling = !rolling;
	}
	if (rolling){
		// Stop rolling
		glutIdleFunc(idle);
	}
	else{
		glutIdleFunc(NULL);
	}
}
//----------------------------------------------------------------------------
void setDefaultView(){
	// initial viewer position
	eye = init_eye;
}
void quit(){
	delete[] vectors;
	delete[] rotationAxis;
	//	for (int i = 0; i<128; i++){
	//		delete sphereData[i];
	//	}
	//delete sphereData;
	//	delete[] sphereData;
	delete[]sphereData;
	delete[]sphere_color;
	exit(1);
}
void main_menu(int index)
{
	switch (index)
	{
	case(0) :
	{
		setDefaultView();
		break;
	}
	case(1) :
	{
		quit();
		break;
	}
	}
	display();
}

void addMenu(){
	glutCreateMenu(main_menu);
	glutAddMenuEntry("Default View Point", 0);
	glutAddMenuEntry("Quit", 1);
	glutAttachMenu(GLUT_LEFT_BUTTON);
}
//----------------------------------------------------------------------------
void reshape(int width, int height)
{
	glViewport(0, 0, width, height);
	aspect = (GLfloat)width / (GLfloat)height;
	glutPostRedisplay();
}
//----------------------------------------------------------------------------
int main(int argc, char **argv)
{
	int err;

	readFiles();
	glutInit(&argc, argv);
	glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH);
	glutInitWindowSize(512, 512);
	// glutInitContextVersion(3, 2);
	// glutInitContextProfile(GLUT_CORE_PROFILE);
	glutCreateWindow("Rolling Ball");
	addMenu();
	/* Call glewInit() and error checking */
	err = glewInit();
	if (GLEW_OK != err)
	{
		printf("Error: glewInit failed: %s\n", (char*)glewGetErrorString(err));
		exit(1);
	}
	glutDisplayFunc(display);
	glutReshapeFunc(reshape);
	//glutIdleFunc(idle);
	glutMouseFunc(mouse);
	glutKeyboardFunc(keyboard);

	init();
	glutMainLoop();

	//	delete sphereData;
	delete[]sphereData;
	delete[]sphere_color;

	return 0;
}

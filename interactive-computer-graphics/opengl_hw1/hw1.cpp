#define WINDOWS     1 /* Set to 1 for Windows, 0 else */
#define UNIX_LINUX  0 /* Set to 1 for Unix/Linux, 0 else */

#if WINDOWS
#include <windows.h>
#include <GL/glut.h>
#endif
#if UNIX_LINUX
#include <GL/gl.h>
#include <GL/glu.h>
#include <GL/glut.h>
#endif
#include <math.h>
#include <iostream>
#include <fstream>
#include <stdlib.h>
#include <stdio.h>
#include <vector>
using namespace std;
#define XOFF          50
#define YOFF          50
#define WINDOW_WIDTH  600
#define WINDOW_HEIGHT 600

int trans_base_x=300; //half the window_width
int trans_base_y=300; //half the window_height
int trans_parameter=1; 
bool animation=0;
int frame_k=1;

struct point
{
	int x_coord;
	int y_coord;
};

struct circle
{
	int center_x;
	int center_y;
	int radius;
};

vector<circle> data_circle;//record the data of circles

void display(void);
void myinit(void);
/*Function to draw one circle*/
void draw_circle(int x, int y, int r);
/*Function to draw 8 points*/
void draw_eight_p(int x, int y,point p);
//Function to draw 1 point
void draw_one_p(int x,int y);
//Function to determine choose SE or E
bool count_diff(point p,int r);
//Receive command
void command();
//Transform the coordinate to fix the screen size
void trans_coord();
//For animation
void idle();
/* Function to handle file input; modification may be needed */
void file_in();

/*-----------------
The main function
------------------*/
int main(int argc, char **argv)
{
    glutInit(&argc, argv);

    /* Use both double buffering and Z buffer */
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH);
    glutInitWindowPosition(XOFF, YOFF);
    glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT);
    glutCreateWindow("CS6533 Assignment 1");
	cout<<"press 1 for input circle's data,( center_x,center_y,radius))"<<endl;
    cout<<"press 2 for draw circle form the data in file.txt"<<endl;
    cout<<"press 3 for animation"<<endl;

    command();
	glutDisplayFunc(display);
	trans_coord();

    myinit();
    glutMainLoop();
}

/*----------
file_in(): file input function. Modify here.
------------*/
void file_in(void)
{
	char* file_path=new char[128];
	file_path="file.txt";
	ifstream file(file_path);
	if(file.fail()) {cout<<"open fail"<<endl;}
	int circle_num=0;
	file >> circle_num;
	cout<<"record numbers:"<<circle_num<<endl;
	while(!file.eof()){
		circle tmp_circle;
		file >> tmp_circle.center_x;
		file >> tmp_circle.center_y;
		file >> tmp_circle.radius;
		data_circle.push_back(tmp_circle);
	}
	cout<<"read over"<<endl;
}


/*---------------------------------------------------------------------
display(): This function is called once for _every_ frame. 
---------------------------------------------------------------------*/
void display(void)
{
  glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
    
  glColor3f(1.0, 0.84, 0);              /* draw in golden yellow */
  glPointSize(1.0);                     /* size of each point */

  for(int i=0;i<data_circle.size();i++)
  {
	  float tmp_diff=0.11;
	  glColor3f(1.0-tmp_diff*i,0.84-tmp_diff*i,tmp_diff*i); //change color slightly
	  int tmp_r=data_circle[i].radius;
	  if(animation==1)
	  {
		  tmp_r=tmp_r*frame_k/10;
	  }
	  draw_circle(data_circle[i].center_x/trans_parameter,data_circle[i].center_y/trans_parameter,tmp_r/trans_parameter);
  }

  glFlush();                            /* render graphics */
  glutSwapBuffers();                    /* swap buffers */
}

/*---------------------------------------------------------------------
myinit(): Set up attributes and viewing
---------------------------------------------------------------------*/
void myinit()
{
  glClearColor(0.0, 0.0, 0.92, 0.0);    /* blue background*/

  /* set up viewing */
  glMatrixMode(GL_PROJECTION);
  glLoadIdentity();
  gluOrtho2D(0.0, WINDOW_WIDTH, 0.0, WINDOW_HEIGHT);
  glMatrixMode(GL_MODELVIEW);
  
}
//receive command from user
void command()
{
	cin.sync();
	char com='0';
	cin>>com;
	switch(com)
	{
	case '1':   //user input the coordination and radius
		{int c_x,c_y,c_r;
		cout<<"Please input center x"<<endl;
		cin>>c_x;
		cout<<"Please input center y"<<endl;
		cin>>c_y;
		cout<<"Please input radius"<<endl;
		cin>>c_r;
		circle tmp_circle={c_x,c_y,c_r};
		data_circle.push_back(tmp_circle);
		break;}
	case '2':   //print the circles from a file
		{file_in();break;}
	case '3':   //add animation
		{file_in();
		animation=1;
		glutIdleFunc(idle);
		break;
		}
	}
}
void trans_coord()
{
	if(data_circle.size()==1)//draw 1 circle
	{
		int tmp_x_max= abs(data_circle[0].center_x)+data_circle[0].radius;
		int tmp_y_max= abs(data_circle[0].center_y)+data_circle[0].radius;
		int coord_max= tmp_x_max>tmp_y_max?tmp_x_max:tmp_y_max;
		if (coord_max>300)
		{
			trans_parameter=int(ceil(coord_max/300.0));
		}
	}
	else //draw more circles
	{
		for(int i=0;i<data_circle.size();i++)
		{
			int tmp_trans_parameter=0;
			int tmp_x_max= abs(data_circle[i].center_x)+data_circle[i].radius;
		    int tmp_y_max= abs(data_circle[i].center_y)+data_circle[i].radius;
		    int coord_max= tmp_x_max>tmp_y_max?tmp_x_max:tmp_y_max;
		    if (coord_max>300)
		    {
			    tmp_trans_parameter=int(ceil(coord_max/300.0));
		    }
			if (tmp_trans_parameter>trans_parameter) {trans_parameter=tmp_trans_parameter;};
		}
	}
}
/*Function to draw one circle*/
void draw_circle(int x, int y, int r)
{
	cout<<"draw cirle,center:"<<x<<","<<y<<"  radius:"<<r<<endl;
	point point_a={0,r};  // point A
	point point_b={r/sqrt(2.0),r/sqrt(2.0)};  //point B
	draw_eight_p(x,y,point_a);
	draw_eight_p(x,y,point_b);
	int init_x=0;
	int init_y=r;
	while(init_x<point_b.x_coord)
	{
		point tmp;
		tmp.x_coord=init_x+1;
		tmp.y_coord=init_y-0.5;  //current point is (x,y),E=(x+1,y),SE=(x+1,y-1),determine if mid point of E and SE is inside the circle
		if(count_diff(tmp,r))
			init_y--;
		tmp.y_coord=init_y;
		draw_eight_p(x,y,tmp);
		init_x++;
	}
}
/*Function to draw 8 points*/
void draw_eight_p(int x, int y, point p)
{
	glBegin(GL_POINTS);
	draw_one_p(x+p.x_coord,y+p.y_coord);
	draw_one_p(x-p.x_coord,y+p.y_coord);
	draw_one_p(x-p.x_coord,y-p.y_coord);
	draw_one_p(x+p.x_coord,y-p.y_coord);
	draw_one_p(x+p.y_coord,y+p.x_coord);
	draw_one_p(x-p.y_coord,y+p.x_coord);
	draw_one_p(x+p.y_coord,y-p.x_coord);
	draw_one_p(x-p.y_coord,y-p.x_coord);
	glEnd();
}

void draw_one_p(int x,int y)
{
	glVertex2i(x+trans_base_x,y+trans_base_y);
}

bool count_diff(point p,int r)//if the mid point of SE and E is inside the circle, choose E, else, choose SE.
{
	if ( p.x_coord*p.x_coord + p.y_coord*p.y_coord - r*r < 0)
		return false;
	else
	    return true;
}

void idle(void) //to determine the size of this frame
{
	frame_k++;
	Sleep(500);
	if(frame_k==10) {frame_k=1;}
	glutPostRedisplay();
}
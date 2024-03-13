/*********************************************
 * OPL 12.10.0.0 Model
 * Author: sjkan
 * Creation Date: 2020. 6. 13. at ���� 1:47:18
 *********************************************/
/*********************************************
 * OPL 12.10.0.0 Model
 * Author: sjkan
 * Creation Date: 2020. 6. 12. at ���� 1:44:35
 *********************************************/
int m = 452; // ���α� ǥ�س���� ���� = 452
int n = 452;

int start = 121; // start node�� ��ȣ �Է� (index�� �ƴԿ� ����)
int end = 202;   //   end node�� ��ȣ �Է� (index�� �ƴԿ� ����)

range ms = 1..m;
range ns = 1..n;

float coefficient[ms][ns] = ...; // ������ t(=0),x(=3),y(=1),z(=2)������ (T_ijt1t2 * (1+a_ij)^x * (1+b_ijt1t2)^y * (1+c_t1t2)^z)
int e_ij[ms][ns]=...;            // node i���� j�� ����� ��ũ�� �ִ��� �Ǻ��ϴ� boolean var

dvar boolean X_ij[ms][ns];       // ���� ��ο��� node i���� j�� ����� ��ũ�� ���ϴ����� �����ִ� boolean ��������

minimize sum(p in ms, q in ns) coefficient[p][q]*X_ij[p][q]; // minimize z = sum(i)sum(j)(T_ijt1t2 * (1+a_ij)^x * (1+b_ijt1t2)^y * (1+c_t1t2)^z) * X_ij 


subject to																							 // flow-conservaton constraint
{

  1 + sum(i in ms) (e_ij[i][start]*X_ij[i][start]) == sum(a in ns) (e_ij[start][a]*X_ij[start][a]);  //  start node����
  sum(i in ms) (e_ij[i][end]*X_ij[i][end]) == sum(a in ns) (e_ij[end][a]*X_ij[end][a]) + 1;			 //    end node����
  
  forall (j in ns : j != start && j != end)															 //�̿��� ��� node���� 
      sum(i in ms) (e_ij[i][j]*X_ij[i][j]) == sum(a in ns) (e_ij[j][a]*X_ij[j][a]);					 
}
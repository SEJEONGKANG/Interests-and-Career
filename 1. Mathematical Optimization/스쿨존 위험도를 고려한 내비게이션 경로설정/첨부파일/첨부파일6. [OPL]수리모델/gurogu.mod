/*********************************************
 * OPL 12.10.0.0 Model
 * Author: sjkan
 * Creation Date: 2020. 6. 13. at 오전 1:47:18
 *********************************************/
/*********************************************
 * OPL 12.10.0.0 Model
 * Author: sjkan
 * Creation Date: 2020. 6. 12. at 오후 1:44:35
 *********************************************/
int m = 452; // 구로구 표준노드의 개수 = 452
int n = 452;

int start = 121; // start node의 번호 입력 (index가 아님에 주의)
int end = 202;   //   end node의 번호 입력 (index가 아님에 주의)

range ms = 1..m;
range ns = 1..n;

float coefficient[ms][ns] = ...; // 지정한 t(=0),x(=3),y(=1),z(=2)에서의 (T_ijt1t2 * (1+a_ij)^x * (1+b_ijt1t2)^y * (1+c_t1t2)^z)
int e_ij[ms][ns]=...;            // node i에서 j로 연결된 링크가 있는지 판별하는 boolean var

dvar boolean X_ij[ms][ns];       // 선정 경로에서 node i에서 j로 연결된 링크를 택하는지를 보여주는 boolean 결정변수

minimize sum(p in ms, q in ns) coefficient[p][q]*X_ij[p][q]; // minimize z = sum(i)sum(j)(T_ijt1t2 * (1+a_ij)^x * (1+b_ijt1t2)^y * (1+c_t1t2)^z) * X_ij 


subject to																							 // flow-conservaton constraint
{

  1 + sum(i in ms) (e_ij[i][start]*X_ij[i][start]) == sum(a in ns) (e_ij[start][a]*X_ij[start][a]);  //  start node에서
  sum(i in ms) (e_ij[i][end]*X_ij[i][end]) == sum(a in ns) (e_ij[end][a]*X_ij[end][a]) + 1;			 //    end node에서
  
  forall (j in ns : j != start && j != end)															 //이외의 모든 node에서 
      sum(i in ms) (e_ij[i][j]*X_ij[i][j]) == sum(a in ns) (e_ij[j][a]*X_ij[j][a]);					 
}
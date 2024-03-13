import React, { useState } from 'react';
import { makeStyles } from '@material-ui/core/styles';
import { TextField,Button,Container,Typography,Box,Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper } from '@mui/material';
import { DashboardLayout } from '../components/dashboard-layout';

const useStyles = makeStyles((theme) => ({
  container: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
    margin: '50px',
  },
  buttonContainer: {
    display: 'flex',
    flexDirection: 'row',
    margin: '10px',
    alignItems: 'center',
  },
  button: {
    margin: '10px',
  },
  formContainer: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    margin: '10px 0',
  },
  textField: {
    width: '500px',
  },
  table: {
    minWidth:650,
  }
}));
const Page = (props) => {
  const classes = useStyles();
  const [selectedIndustry, setSelectedIndustry] = useState('');
  const [item, setItem] = useState('');
  const [loading, setLoading] = useState(false);
  const [recieve, setRecieve] = useState(false);
  const [recommendation,setRecommendation]=useState([]);
  const [similarity, setSimilarity]=useState([]);
  const handleButtonClick = (industry) => {
    setSelectedIndustry(industry);
  };
  const handleSubmit = async(e) => {
    const lst1 = [];
    const lst2 = [];
    setLoading(true);
    e.preventDefault();
    alert(`다음과 같은 아이템을 제출하였습니다: ${item}`);
    const formData = new FormData();
    formData.append('item',item);
    formData.append('industry',selectedIndustry);
    const res1 = await fetch('http://localhost:5000/rdtogether/reco', {
      method: 'POST',
      body:formData});
    const res2 = await fetch('http://localhost:5000/rdtogether/similar', {
        method: 'POST',
        body:formData
    });
    const data1 = await res1.json();
    const data2 = await res2.json();
    lst1.push(data1.r0,data1.r1,data1.r2,data1.r3,data1.r4)
    lst2.push(data2.s0,data2.s1,data2.s2,data2.s3,data2.s4)
    setRecommendation(lst1);
    console.log(recommendation);
    setSimilarity(lst2);
    setLoading(false);
    setRecieve(true);
  };
  const show1=[]
  const show2=[]
  for (let i=0; i<recommendation.length; i++) {
    show1.push({
              departmentname:recommendation[i][0],
              title:recommendation[i][1],
              duedate:recommendation[i][2],
              adepartment:recommendation[i][3],
              url:recommendation[i][4],
              type:recommendation[i][5],
              money:recommendation[i][6],
              field:recommendation[i][7]})
  }
  for (let i=0; i<similarity.length; i++){
    show2.push({
                title:similarity[i][0]})
  };
  const projects = show1;
  const products = show2;
  
  function ProjectsTable() {
    const classes = useStyles();
  
    return (
      <>
      
      <TableContainer title='지원과제추천' component={Paper} style={{ marginRight: "30px" }}>
        <Table className={classes.table} aria-label="projects table">
          <TableHead >
            <TableRow>
              <TableCell align="center">부처명</TableCell>
              <TableCell align="center">제목</TableCell>
              <TableCell align="center">마감일</TableCell>
              <TableCell align="center">공고부서</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {projects.map((project, index) => (
              <TableRow key={index}>
                <TableCell component="th" scope="row" align="center">{project.departmentname}</TableCell>
                <TableCell align="center">{project.title}</TableCell>
                <TableCell align="center">{project.duedate}</TableCell>
                <TableCell align="center">{project.adepartment}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
      
      </>);
  }
  
  function ProductsTable() {
    const classes = useStyles();  
    return (
      <>
      
      <TableContainer title='유사과제정보' component={Paper} style={{ marginLeft: "30px" }}>
        <Table className={classes.table} aria-label="products table">
          <TableHead>
            <TableRow>
              <TableCell align="center">제목</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {products.map((product, index) => (
              <TableRow key={index}>
                <TableCell align="center">{product.title}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
      </>
    );
  };




  if (!recieve && !loading) return (
    <Box sx={{
      display: 'flex',
      flex: '1 1 auto',
      flexDirection: 'column',
      width: '100%'
    }}>
    <Box {...props}>
      <Typography
        variant="h4"
      >
        R&D Together
      </Typography>
    </Box>
    <Box
      component="main"
      sx={{
        flexGrow: 1,
        py: 8
      }}>
    <Container>
        <Button
          variant="contained"
          color="primary"
          className={classes.button}
          onClick={() => handleButtonClick('기계, 소재')}
        >
          기계, 소재
        </Button>
        <Button
          variant="contained"
          color="primary"
          className={classes.button}
          onClick={() => handleButtonClick('전기, 전자')}
        >
          전기, 전자
        </Button>
        <Button
          variant="contained"
          color="primary"
          className={classes.button}
          onClick={() => handleButtonClick('정보통신')}
        >
          정보통신
        </Button>
        <Button
          variant="contained"
          color="primary"
          className={classes.button}
          onClick={() => handleButtonClick('화학')}
        >
          화학
        </Button>
        <Button
          variant="contained"
          color="primary"
          className={classes.button}
          onClick={() => handleButtonClick('바이오, 의료')}
        >
          바이오, 의료
        </Button>
        <Button
          variant="contained"
          color="primary"
          className={classes.button}
          onClick={() => handleButtonClick('에너지, 자원')}
        >
          에너지, 자원
        </Button>
        <Button
          variant="contained"
          color="primary"
          className={classes.button}
          onClick={() => handleButtonClick('지식서비스')}
          >
            지식서비스
          </Button>
        </Container>
      
        <div className={classes.formContainer}>
          <Typography variant="h4">현재 기업에서 개발중인 아이템을 작성해주세요.</Typography>
          <form onSubmit={handleSubmit}>
            <TextField
              label="Item"
              variant="outlined"
              className={classes.textField}
              value={item}
              onChange={(e) => setItem(e.target.value)}
              rows={4}
              cols={50}
              multiline
            />
            <Button type="submit" variant="contained" color="primary">
              Submit
            </Button>
          </form>
        </div>
      
        <Typography variant="h5">
          선택된 사업분야: {selectedIndustry ? selectedIndustry : 'None'}
        </Typography>
      </Box></Box>
      );
    if (loading) return(<></>);
    if (!loading) return (
      <Box style={{ display: "flex", justifyContent: "center" }}>
        <ProjectsTable />
        <ProductsTable />
      </Box>
    );
    };
      
      
      Page.getLayout = (page) => (
        <DashboardLayout>
          {page}
        </DashboardLayout>
      );
export default Page;
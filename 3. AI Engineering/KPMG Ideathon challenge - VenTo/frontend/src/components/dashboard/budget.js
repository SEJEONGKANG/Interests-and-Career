import { Avatar, Box, Card, CardContent, Grid, Typography, Divider, CardActions, Button } from '@mui/material';
import ArrowDownwardIcon from '@mui/icons-material/ArrowDownward';
import MoneyIcon from '@mui/icons-material/Money';
import GavelIcon from '@mui/icons-material/Gavel';
import LanguageIcon from '@mui/icons-material/Language';
import BiotechIcon from '@mui/icons-material/Biotech';




export const Budget = (props) => (
  <Grid sx={{ display: 'flex', justifyContent: 'space-between', marginX: '60x' }}>
    <Grid item xs={120} sm={40}>
    <Card {...props}
      sx={{
        alignItems: 'center',
        display: 'flex',
        flexDirection: 'column',
        height: 600,
        width: 300,
        marginX: '10px',
      }}
    >
        <CardContent>
          <Box
            sx={{
              alignItems: 'center',
              display: 'flex',
              flexDirection: 'column',
              height:300,
              width:300
            }}
          >

            <BiotechIcon 
                          sx={{
                            height: 64,
                            mb: 2,
                            width: 64
                          }}/>

            <Typography
              color="textPrimary"
              gutterBottom
              variant="h5"
            >
              R&D Together
            </Typography>
            <Box  sx={{ width: '75%'}}>
            <Typography
              color="textSecondary"
              variant="body2"
            >
              기업 자금에 기반이 될 딱 맞는 정부지원 과제 추천 서비스
            </Typography>
            </Box>
          </Box>
        </CardContent>
        <Divider />
        <CardActions>
          <Button
            color="primary"
            fullWidth
            variant="text"
          >
            자세히 알아보기
          </Button>
        </CardActions>
      </Card>
    </Grid>

    <Grid item xs={12} sm={40}>
    <Card {...props}
      sx={{
        alignItems: 'center',
        display: 'flex',
        flexDirection: 'column',
        height: 600,
        width: 300,
        marginX: '10px',
      }}
    >
        <CardContent>
          <Box
            sx={{
              alignItems: 'center',
              display: 'flex',
              flexDirection: 'column',
              height:300,
              width:300
            }}
          >
            <GavelIcon 
                          sx={{
                            height: 64,
                            mb: 2,
                            width: 64
                          }}/>
            <Typography
              color="textPrimary"
              gutterBottom
              variant="h5"
            >
              Contract Together
            </Typography>
            <Box  sx={ {width: '75%'} }>
            <Typography
              color="textSecondary"
              variant="body2"
            >
              국내외 계약서가 잘 작성되었는지 걱정될 땐 계약서 내 유불리 조항 판별 서비스
            </Typography>
            </Box>
          </Box>
        </CardContent>
        <Divider />
        <CardActions>
          <Button
            color="primary"
            fullWidth
            variant="text"
          >
            자세히 알아보기
          </Button>
        </CardActions>
      </Card>
    </Grid>

    <Grid item xs={120} sm={40}>
    <Card {...props}
      sx={{
        alignItems: 'center',
        display: 'flex',
        flexDirection: 'column',
        height: 600,
        width: 300,
        marginX: '10px',
      }}
    >
        <CardContent>
          <Box
            sx={{
              alignItems: 'center',
              display: 'flex',
              flexDirection: 'column',
              height:300,
              width:300
            }}
          >
            <LanguageIcon 
                          sx={{
                            height: 64,
                            mb: 2,
                            width: 64
                          }}/>
            <Typography
              color="textPrimary"
              gutterBottom
              variant="h5"
            >
              Issue Together
            </Typography>
            <Box  sx={{ width: '75%'}}>
            <Typography
              color="textSecondary"
              variant="body2"
            >
              우리 기업에 필요한 이슈 및 해외 정보 제공 서비스
            </Typography>
            </Box>
          </Box>
        </CardContent>
        <Divider />
        <CardActions>
          <Button
            color="primary"
            fullWidth
            variant="text"
          >
            자세히 알아보기
          </Button>
        </CardActions>
      </Card>
    </Grid>
    </Grid>
);

export default Budget;
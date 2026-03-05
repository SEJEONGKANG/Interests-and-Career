import { useState } from 'react';
import {
  Box,
  Button,
  Card,
  CardContent,
  TextField,
  InputAdornment,
  SvgIcon,
  Typography
} from '@mui/material';
import { Download as DownloadIcon } from '../../icons/download';
import { Search as SearchIcon } from '../../icons/search';
import { Upload as UploadIcon } from '../../icons/upload';
import NextLink from 'next/link';
import MetadataDashboard from './MetadataDashboard';

export const ProductListToolbar = (props) => {
  const [inputText, setInputText] = useState('');
  const [result, setResult] = useState(null); // initialize the result as null

  const handleInputChange = (event) => {
    setInputText(event.target.value);
  };

  const handleSearchClick = async () => {
    const formData = new FormData();
    formData.append('company_name', inputText);

    const response = await fetch('http://127.0.0.1:5000/issuetogether', {
      method: 'POST',
      body: formData
    });

    const products = await response.json();

    setResult(products); // set the result to the parsed object
    console.log(products);
  };

  return (
    <Box {...props}>
      <Box
        sx={{
          alignItems: 'center',
          display: 'flex',
          justifyContent: 'space-between',
          flexWrap: 'wrap',
          m: -1
        }}
      >
        <Typography sx={{ m: 1 }} variant="h4">
          Issue Together
        </Typography>

      </Box>
      <Box sx={{ mt: 3 }}>
        <Card>
          <CardContent>
            <Box sx={{ maxWidth: 500 }}>
              <TextField
                fullWidth
                InputProps={{
                  startAdornment: (
                    <InputAdornment position="start">
                      <SvgIcon fontSize="small" color="action">
                        <SearchIcon />
                      </SvgIcon>
                    </InputAdornment>
                  )
                }}
                placeholder="기업명을 입력해주세요"
                variant="outlined"
                value={inputText}
                onChange={handleInputChange}
              />
              <Button
                variant="contained"
                color="primary"
                onClick={handleSearchClick}
                sx={{ mt: 2 }}
              >
                검색
              </Button>
            </Box>
          </CardContent>
        </Card>
        {result && (
          <MetadataDashboard
            products={Object.keys(result).map((key) => {
              return {
                url: result[key].url,
                urlToImage: result[key].urlToImage,
                source: result[key].source,
                title: result[key].title
              };
            })}
          />
        )}
      </Box>
    </Box>
  );
};


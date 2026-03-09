import { useState } from 'react';
import {
  Box,
  Button,
  Card,
  CardContent,
  TextField,
  InputAdornment,
  SvgIcon,
  Typography,
  Slider
} from '@mui/material';
import { Search as SearchIcon } from '../../icons/search';
import { Upload as UploadIcon } from '../../icons/upload';
import { Download as DownloadIcon } from '../../icons/download';

export const CustomerListToolbar = (props) => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [previewImage, setPreviewImage] = useState(null);
  const [result, setResult] = useState(null);
  const [attention, setAttention] = useState(null);
  const [sliderValue, setSliderValue] = useState(0);

  const handleFileSelect = (event) => {
    setSelectedFile(event.target.files[0]);
    setPreviewImage(URL.createObjectURL(event.target.files[0]));
  };

  const handleFileUpload = async () => {
    const formData = new FormData();
    formData.append('file', selectedFile);
    formData.append('sliderValue', sliderValue);
    const response = await fetch('http://127.0.0.1:5000/contracttogether', {
      method: 'POST',
      body: formData
    });
    const data = await response.json();
    setResult(data.sentences);
    setAttention(data.attention);
    console.log(data.attention)
  };

  const handleButtonClick = async () => {
    if (selectedFile) {
      await handleFileUpload();
    }
    handleShowResult();
  };

  const handleShowResult = () => {
    console.log(result)
    if (result) {
      window.open(`/result?value=${result}`);
    }
  };

  const handleSliderChange = (event, newValue) => {
    setSliderValue(newValue.toFixed(2));
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
        <Typography
          sx={{ m: 1 }}
          variant="h4"
        >
          ContractTogether
        </Typography>
        <Box sx={{ m: 1 }}>
          <Button
            startIcon={<UploadIcon fontSize="small" />}
            sx={{ mr: 1 }}
            color="primary"
            variant="contained"
            component="label"
          >
            계약서 업로드(Pdf)
            <input
              type="file"
              hidden
              onChange={handleFileSelect}
            />
          </Button>
        </Box>

      </Box>

      {previewImage && (
        <Box sx={{ mt: 3 }}>
          <img src={previewImage} alt="PDF preview" width="300" />
        </Box>
      )}
      {selectedFile && (
        <Typography sx={{ mt: 3 }}>
          파일명: {selectedFile.name}
        </Typography>
      )}
      <Box sx={{ mt: 3 }}>
        <Typography id="sliderLabel">
          Threshold: {sliderValue}
        </Typography>
        <Slider
          aria-labelledby="sliderLabel"
          value={Number(sliderValue)}
          min={0.5}
          max={1}
          step={0.01}
          onChange={handleSliderChange}
          sx={{ width: 200 }}
        />
      </Box>

      <Box sx={{ m: 1 }}>
      <Button
            startIcon={<SearchIcon fontSize="small" />}
            sx={{ mr: 1 }}
            color="primary"
            variant="contained"
            onClick={handleButtonClick}
            disabled={!selectedFile}
          >
            {result ? '결과보기' : '불리한 조항 검출'}
          </Button>
        </Box>

      {result && result.map((sentence, index) => (
        <Typography key={index} sx={{ mt: 3 }}>
          불리한 조항 {index + 1}
          <br />
          {String(sentence).substring(0, String(sentence).indexOf(')') + 1)}
          <br />
          {index === 0 && attention.map((score, i) => (
            <span key={i} style={{ backgroundColor: 'rgba(255, 0, 0, ' + score + ')' }}>
              {String(sentence).charAt(i + String(sentence).indexOf(')') + 2)}
            </span>
          ))}
          {index !== 0 && String(sentence).substring(String(sentence).indexOf(')') + 2)}
        </Typography>
      ))}
      

    </Box>
  );
};      
import React from 'react';
import { Typography, Box, Card, CardContent, CardMedia, Avatar } from '@mui/material';

const MetadataDashboard = ({ products }) => {
  const groupsOfThree = [];
  for (let i = 0; i < Object.keys(products).length; i += 3) {
    const group = [];
    for (let j = 0; j < 3; j++) {
      const index = i + j;
      if (index < Object.keys(products).length) {
        group.push(products[Object.keys(products)[index]]);
      }
    }
    groupsOfThree.push(group);
  }

  return (
    <Box sx={{ mt: 3 }}>
      <Typography variant="h6">News Dashboard</Typography>
 
      {groupsOfThree.map((group, i) => (
        <Box key={i} sx={{ display: 'flex', gap: 2, mt: 2 }}>
          {group.map((product) => (
            <Card key={product.source} sx={{ maxWidth: 300 }}>
              <CardMedia component="img" height="140" image={product.urlToImage} alt={product.title} />
              <a href={product.url} target="_blank" rel="noreferrer">
                <CardContent>
                  <Typography gutterBottom variant="h6" component="div">
                    {product.title}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Source: {product.source}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    URL: {product.url}
                  </Typography>
                </CardContent>
              </a>
            </Card>
          ))}
        </Box>
      ))}
    </Box>
  );
};

export default MetadataDashboard;

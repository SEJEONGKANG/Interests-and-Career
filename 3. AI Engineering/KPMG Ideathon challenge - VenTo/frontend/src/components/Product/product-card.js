import { useEffect, useState } from 'react';
import {
  Box,
  Card,
  CardContent,
  Grid,
  Typography,
} from '@mui/material';
//import { ProductCard } from './ProductCard';
//import { Loading } from '../../components/Loading';
//import { Error } from '../../components/Error';

export const ProductList = () => {
  const [products, setProducts] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    setIsLoading(true);
    fetch('https://fakestoreapi.com/products')
      .then(response => response.json())
      .then(data => {
        setProducts(data);
        setIsLoading(false);
      })
      .catch(error => {
        setIsLoading(false);
        setError(error);
      });
  }, []);

  return (
    <Box sx={{ flexGrow: 1 }}>
      {isLoading && <Loading />}
      {error && <Error message={error.message} />}
      {!isLoading && !error && (
        <>
          <Typography variant="h4" gutterBottom>
            Products
          </Typography>
          <Box sx={{ mb: 2 }}>
            <Grid container spacing={2}>
              {products.map((product) => (
                <Grid item key={product.id} xs={12} sm={6} md={4} lg={3}>
                  <ProductCard product={product} />
                </Grid>
              ))}
            </Grid>
          </Box>
        </>
      )}
    </Box>
  );
};

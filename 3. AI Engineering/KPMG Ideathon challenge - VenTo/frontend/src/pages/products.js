import { Container } from '@mui/material';
import { ProductListToolbar } from '../components/product/product-list-toolbar';
import MetadataDashboard from '../components/product/MetadataDashboard';
import { DashboardLayout } from '../components/dashboard-layout';


const Page = () => {
  return (
    <Container maxWidth="lg">
      <ProductListToolbar />
      {/* You can pass the result state as a prop to the MetadataDashboard component */}
      {/* <MetadataDashboard products={result} /> */}
    </Container>
  );
};

Page.getLayout = (page) => (
  <DashboardLayout>
    {page}
  </DashboardLayout>
);

export default Page;

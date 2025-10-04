import React from 'react';
import { Box, Container, Grid, Link, Typography, Stack } from '@mui/material';
import { Link as RouterLink } from 'react-router-dom';

export const Footer: React.FC = () => {
  return (
    <Box component="footer" sx={{ mt: 'auto', py: 4, borderTop: '1px solid', borderColor: 'divider', bgcolor: 'background.paper' }}>
      <Container maxWidth="lg">
        <Grid container spacing={3}>
          <Grid item xs={12} md={4}>
            <Typography variant="subtitle1" sx={{ fontWeight: 700, mb: 1, color: 'text.primary' }}>About</Typography>
            <Stack spacing={0.5}>
              <Link component={RouterLink} to="/about" underline="none">Project</Link>
              <Link href="https://sunsetsocialmedia.wordpress.com" target="_blank" rel="noopener" underline="none">Blog</Link>
            </Stack>
          </Grid>
          <Grid item xs={12} md={4}>
            <Typography variant="subtitle1" sx={{ fontWeight: 700, mb: 1, color: 'text.primary' }}>Contact</Typography>
            <Stack spacing={0.5}>
              <Typography variant="body2"><Link href="mailto:basunimohannad@gmail.com" underline="none">basunimohannad@gmail.com</Link></Typography>
              <Typography variant="body2"><Link href="tel:0569074125" underline="none">0569074125</Link></Typography>
            </Stack>
          </Grid>
          <Grid item xs={12} md={4}>
            <Typography variant="subtitle1" sx={{ fontWeight: 700, mb: 1, color: 'text.primary' }}>Social</Typography>
            <Stack spacing={0.5}>
              <Link href="https://www.linkedin.com/in/mohannad-basyouni" target="_blank" rel="noopener" underline="none">LinkedIn</Link>
              <Link href="https://github.com/HannoodCode" target="_blank" rel="noopener" underline="none">GitHub</Link>
            </Stack>
          </Grid>
        </Grid>
        <Box sx={{ mt: 3, textAlign: 'center' }}>
          <Typography variant="caption" color="text.secondary">
            © {new Date().getFullYear()} AI Speech Pipeline. Made by{' '}
            <Link 
              href="https://www.linkedin.com/in/mohannad-basyouni" 
              target="_blank" 
              rel="noopener" 
              underline="none"
              sx={{ color: 'text.secondary', fontWeight: 600 }}
            >
              Mohannad Basyouni
            </Link>
          </Typography>
        </Box>
      </Container>
    </Box>
  );
};

export default Footer;



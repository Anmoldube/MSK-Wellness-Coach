# 🚀 Deployment Checklist

## Pre-Deployment

### Environment Configuration
- [ ] Copy `.env.example` to `.env`
- [ ] Set `DEBUG=false` in production
- [ ] Configure production database URL
- [ ] Add Anthropic API key (optional, works without it)
- [ ] Set proper `ALLOWED_ORIGINS` for CORS
- [ ] Configure `LOG_LEVEL=ERROR` for production

### Database
- [ ] PostgreSQL 15+ installed and running
- [ ] Database created: `msk_chatbot`
- [ ] User created with proper permissions
- [ ] Run database migrations: `alembic upgrade head`
- [ ] Test database connection
- [ ] Set up automated backups

### Security
- [ ] Change default database passwords
- [ ] Configure HTTPS/SSL certificates
- [ ] Set up firewall rules
- [ ] Review CORS settings
- [ ] Enable rate limiting (`RATE_LIMIT_ENABLED=true`)
- [ ] Configure proper file upload size limits

### Infrastructure
- [ ] Docker and Docker Compose installed
- [ ] Sufficient disk space for uploads and ChromaDB
- [ ] Create data directories with proper permissions:
  - `./data/uploads`
  - `./data/chromadb`

## Deployment Steps

### Using Docker Compose (Recommended)

1. **Build images**
```bash
docker-compose build
```

2. **Start services**
```bash
docker-compose up -d
```

3. **Check health**
```bash
curl http://localhost:8000/health
```

4. **View logs**
```bash
docker-compose logs -f
```

### Manual Deployment

#### Backend
```bash
cd backend
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

#### Frontend
```bash
cd frontend
npm install
npm run build
# Serve the dist/ folder with nginx or similar
```

## Post-Deployment Testing

### Smoke Tests
- [ ] Frontend loads at production URL
- [ ] API health check returns 200: `/health`
- [ ] API docs accessible: `/docs`
- [ ] Can create user profile
- [ ] Can fetch recommendations
- [ ] Database queries work
- [ ] ChromaDB vector search works
- [ ] File uploads work
- [ ] Progress tracking works

### Performance Tests
- [ ] Response time < 200ms for simple queries
- [ ] Database connection pool configured
- [ ] Rate limiting works (61st request in 1 min fails)
- [ ] Large file uploads work (up to 10MB)

### Monitoring
- [ ] Set up logging aggregation (ELK, CloudWatch, etc.)
- [ ] Configure error alerting
- [ ] Monitor database connections
- [ ] Track API response times
- [ ] Monitor disk space (uploads/ChromaDB)
- [ ] Set up uptime monitoring

## Production Hardening

### Security Hardening
- [ ] Run security scan on Docker images
- [ ] Update all dependencies to latest secure versions
- [ ] Implement API authentication (if needed)
- [ ] Add request size limits
- [ ] Configure security headers
- [ ] Enable SQL injection protection (SQLAlchemy handles this)
- [ ] Validate file uploads strictly

### Performance Optimization
- [ ] Enable database query caching
- [ ] Configure Redis for session storage (if needed)
- [ ] Set up CDN for static assets
- [ ] Enable gzip compression
- [ ] Optimize ChromaDB collection size
- [ ] Configure database indexes

### Backup Strategy
- [ ] Automated daily PostgreSQL backups
- [ ] Backup ChromaDB data directory
- [ ] Backup user uploads directory
- [ ] Test backup restoration process
- [ ] Store backups in separate location
- [ ] Retain backups for 30 days

## Rollback Plan

### If Deployment Fails
```bash
# Stop new version
docker-compose down

# Restore database from backup
psql -U msk_user -d msk_chatbot < backup.sql

# Start previous version
git checkout <previous-version>
docker-compose up -d
```

## Scaling Considerations

### Horizontal Scaling
- [ ] Use load balancer for multiple backend instances
- [ ] Configure shared database for all instances
- [ ] Use shared storage for uploads (S3, etc.)
- [ ] Sync ChromaDB across instances

### Vertical Scaling
- [ ] Increase database resources (CPU, RAM)
- [ ] Increase backend worker count
- [ ] Allocate more disk space for data

## Maintenance

### Weekly
- [ ] Review error logs
- [ ] Check disk space usage
- [ ] Monitor database size
- [ ] Review API usage patterns

### Monthly
- [ ] Update dependencies (security patches)
- [ ] Review and clean old uploads
- [ ] Optimize database (VACUUM, ANALYZE)
- [ ] Test backup restoration

### Quarterly
- [ ] Major dependency updates
- [ ] Security audit
- [ ] Performance review
- [ ] User feedback review

## Emergency Contacts

- **DevOps Lead**: [Name/Contact]
- **Database Admin**: [Name/Contact]
- **Backend Lead**: [Name/Contact]
- **Frontend Lead**: [Name/Contact]

## Useful Commands

### Docker
```bash
# View all logs
docker-compose logs -f

# Restart specific service
docker-compose restart backend

# Check container status
docker-compose ps

# Execute command in container
docker-compose exec backend bash

# View resource usage
docker stats
```

### Database
```bash
# Connect to database
docker-compose exec postgres psql -U msk_user -d msk_chatbot

# Create backup
docker-compose exec postgres pg_dump -U msk_user msk_chatbot > backup.sql

# Restore backup
docker-compose exec -T postgres psql -U msk_user -d msk_chatbot < backup.sql
```

### Migrations
```bash
# Create new migration
docker-compose exec backend alembic revision --autogenerate -m "description"

# Apply migrations
docker-compose exec backend alembic upgrade head

# Rollback migration
docker-compose exec backend alembic downgrade -1
```

## Success Metrics

- [ ] 99.9% uptime
- [ ] < 200ms average response time
- [ ] < 1% error rate
- [ ] All critical endpoints working
- [ ] Database backups running successfully
- [ ] No security vulnerabilities
- [ ] Positive user feedback

---

**Deployment Date**: ___________  
**Deployed By**: ___________  
**Version**: ___________  
**Status**: ☐ Success  ☐ Failed  ☐ Rolled Back

# Mowzf HR Management Suite

A comprehensive Odoo module suite for managing air ticket requests, vacation calculations, and exit-reentry procedures for employees. This module is designed specifically for organizations operating in the Gulf region and handles complex HR scenarios including employee nationalities, sponsorship systems, and regulatory compliance.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Configuration](#configuration)
- [User Guide](#user-guide)
- [Technical Details](#technical-details)
- [Enhancement Plan](#enhancement-plan)
- [Support](#support)

## 🎯 Overview

The Mowzf HR Management Suite consists of three integrated modules organized in the `custom_addons/` directory:

1. **Air Ticket Request** (`custom_addons/air_ticket_request/`) - Manages employee air ticket requests for vacations, business trips, and final exits
2. **End Service Vacation Calculation** (`custom_addons/endservice_vacation_calculation/`) - Handles vacation settlements and service termination calculations
3. **Exit Re-entry Request** (`custom_addons/exit_reentry_request/`) - Manages exit and re-entry visa requests for employees

This suite is particularly suited for companies in Saudi Arabia and Gulf countries where sponsorship systems and specific regulatory requirements apply.

### Project Structure
```
air_ticket_vaccation_fired_19/
├── README.md                    # Main project documentation
├── custom_addons/              # Odoo modules directory
│   ├── air_ticket_request/     # Air ticket management module
│   ├── endservice_vacation_calculation/  # Vacation calculation module
│   └── exit_reentry_request/   # Exit re-entry management module
├── reorganize_modules.sh       # Module reorganization script
└── .git/                       # Git repository
```

> **Note**: If you're upgrading from a previous version where modules were in the root directory, run the `reorganize_modules.sh` script to move them to the `custom_addons/` directory.

## ✨ Features

### Air Ticket Request Module
- **Multi-language Support**: Arabic and English interface
- **Employee Classification**: Native/Non-native nationality handling
- **Flexible Payment Options**: Employee share deduction from salary or cash payment
- **Integration**: Seamless integration with HR leaves and employee records
- **Document Management**: Iqama and passport information tracking
- **Approval Workflow**: Multi-level approval process with tracking
- **Request Types**: Leave, cash allowance, business trips, final exit, and other reasons

### End Service Vacation Calculation
- **Vacation Settlement**: Calculate remaining vacation balances
- **Service Termination**: Handle end-of-service calculations
- **Resignation Processing**: Manage resignation procedures
- **Automatic Calculations**: Days calculation based on service period
- **Multi-currency Support**: Handle different currency requirements
- **Reporting**: Generate settlement reports

### Exit Re-entry Request
- **Document Tracking**: Iqama and passport management
- **Multi-reason Support**: Vacation, emergency, business, medical, family visits
- **Approval Workflow**: Structured approval process
- **Employee Integration**: Direct link to employee records
- **Status Tracking**: Real-time status updates

## 🚀 Installation

### Prerequisites
- Odoo 16.0 or later
- Python 3.8+
- Required Odoo modules: `base`, `mail`, `hr`, `hr_holidays`, `account`

### Installation Steps

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd air_ticket_vaccation_fired_19
   ```

2. **Copy to Odoo addons directory**:
   ```bash
   cp -r custom_addons/air_ticket_request /path/to/odoo/addons/
   cp -r custom_addons/endservice_vacation_calculation /path/to/odoo/addons/
   cp -r custom_addons/exit_reentry_request /path/to/odoo/addons/
   ```

   Alternatively, you can add the `custom_addons` directory directly to your Odoo `addons_path`:
   ```bash
   # In odoo.conf
   addons_path = /path/to/odoo/addons,/path/to/air_ticket_vaccation_fired_19/custom_addons
   ```

3. **Restart Odoo server**:
   ```bash
   sudo systemctl restart odoo
   ```

4. **Install modules**:
   - Navigate to Apps menu in Odoo
   - Update the app list
   - Search for "Air Ticket Request", "Vacation Calculation", and "Exit Reentry"
   - Install each module

### Module Organization

If you have modules in the root directory and want to organize them in `custom_addons/`, run the reorganization script:

```bash
chmod +x reorganize_modules.sh
./reorganize_modules.sh
```

This script will:
- Create the `custom_addons/` directory
- Move all modules into the organized structure
- Create symbolic links for backward compatibility
- Provide installation instructions

## ⚙️ Configuration

### Initial Setup

1. **Access Rights Configuration**:
   - Navigate to Settings → Users & Companies → Groups
   - Configure user access for each module based on roles

2. **Sequence Configuration**:
   - The modules automatically create sequences for request numbering
   - Customize sequences in Settings → Technical → Sequences

3. **Air Ticket Types Setup**:
   - Navigate to HR → Configuration → Air Ticket Types
   - Define different ticket types (economy, business, etc.)

4. **Country and Nationality Setup**:
   - Configure countries in General Settings → Countries
   - Set up nationality classifications

### Company-specific Configuration

1. **Employee Information**:
   - Ensure employee records contain required fields:
     - Iqama number and expiry date
     - Passport number and expiry date
     - Manager assignment
     - Department assignment

2. **Leave Types**:
   - Configure leave types that integrate with air ticket requests
   - Set up allocation rules

## 📚 User Guide

### For Employees

#### Creating an Air Ticket Request

1. **Navigate to HR → Air Ticket Requests**
2. **Click "Create"**
3. **Fill in the form**:
   - Select your employee record
   - Choose request reason (Leave, Business Trip, etc.)
   - Specify travel dates
   - Select ticket type
   - Choose reservation type (Employee only or Employee + Family)

4. **Submit for Approval**:
   - Save the form
   - The request will be sent to your manager for approval

#### Tracking Request Status

- **New**: Request created but not reviewed
- **Reviewed**: Under manager review
- **Approved**: Request approved and processed
- **Refused**: Request denied with reason

### For Managers

#### Reviewing Air Ticket Requests

1. **Navigate to HR → Air Ticket Requests**
2. **Filter by "To Review"**
3. **Open request to review**:
   - Verify employee eligibility
   - Check leave balance integration
   - Review request details
   - Approve or refuse with comments

#### Processing Vacation Calculations

1. **Navigate to HR → Vacation Calculations**
2. **Create new calculation**:
   - Select employee
   - Choose calculation type (Settlement, Termination, Resignation)
   - Set last working date
   - System calculates automatically

### For HR Administrators

#### Managing Exit Re-entry Requests

1. **Monitor all requests** in HR → Exit Re-entry Requests
2. **Process approvals** based on company policy
3. **Track document validity** (Iqama, Passport expiry dates)
4. **Generate reports** for compliance

#### System Maintenance

1. **Regular Data Cleanup**:
   - Archive old requests
   - Update employee information
   - Maintain document validity

2. **Reporting**:
   - Generate monthly/quarterly reports
   - Track approval patterns
   - Monitor compliance metrics

## 🔧 Technical Details

### Module Structure

```
custom_addons/
├── air_ticket_request/
│   ├── __init__.py
│   ├── __manifest__.py
│   ├── controllers/          # Web controllers
│   ├── data/                # XML data files
│   ├── models/              # Python model files
│   ├── security/            # Access rights configuration
│   ├── static/              # Static assets
│   └── views/               # XML view definitions
├── endservice_vacation_calculation/
│   ├── __init__.py
│   ├── __manifest__.py
│   ├── data/                # Sequences and groups
│   ├── models/              # Vacation calculation logic
│   ├── report/              # Report templates
│   ├── security/            # Security configuration
│   └── views/               # View definitions
└── exit_reentry_request/
    ├── __init__.py
    ├── __manifest__.py
    ├── data/                # Sequence configuration
    ├── models/              # Exit-reentry models
    ├── security/            # Access control
    ├── static/              # CSS and assets
    └── views/               # UI definitions
```

### Key Models

- `air.ticket.request` - Main air ticket request model
- `air.ticket.type` - Air ticket type configuration
- `vacation.calculation` - Vacation settlement calculations
- `hr.exit.entry.request` - Exit and re-entry requests
- `exit.reentry.policy` - Exit re-entry policies

### Database Integration

- Seamless integration with Odoo's HR module
- Extends `hr.employee` and `hr.leave` models
- Mail tracking and activity management
- Document attachment support

## 🚀 Enhancement Plan

### Phase 1: Core Improvements (Q1 2024)

#### Performance Optimization
- [ ] Implement database indexing for frequently queried fields
- [ ] Add caching for employee lookup operations
- [ ] Optimize report generation queries

#### User Experience
- [ ] Add dashboard views for managers and HR
- [ ] Implement bulk approval functionality
- [ ] Create mobile-responsive views
- [ ] Add notification system for request updates

#### Integration Enhancements
- [ ] API endpoints for external systems
- [ ] Integration with payroll systems
- [ ] Document scanning and OCR integration
- [ ] Email automation for approvals

### Phase 2: Advanced Features (Q2 2024)

#### Analytics and Reporting
- [ ] Advanced analytics dashboard
- [ ] Predictive analytics for request patterns
- [ ] Cost analysis and budgeting tools
- [ ] Compliance reporting automation

#### Workflow Improvements
- [ ] Configurable approval workflows
- [ ] Delegation support for managers
- [ ] Escalation rules for overdue approvals
- [ ] Batch processing capabilities

#### Document Management
- [ ] Digital signature integration
- [ ] Document version control
- [ ] Automated document generation
- [ ] Compliance document tracking

### Phase 3: Advanced Integration (Q3 2024)

#### External System Integration
- [ ] Government portal integration (Saudi Arabia)
- [ ] Airlines booking system integration
- [ ] Banking system integration for payments
- [ ] Immigration system connectivity

#### AI and Automation
- [ ] Smart request validation
- [ ] Automated eligibility checking
- [ ] Intelligent document processing
- [ ] Predictive request suggestions

#### Multi-company Support
- [ ] Multi-company request handling
- [ ] Cross-company reporting
- [ ] Centralized policy management
- [ ] Group-level analytics

### Phase 4: Enterprise Features (Q4 2024)

#### Advanced Security
- [ ] Two-factor authentication
- [ ] Audit trail enhancements
- [ ] Role-based field encryption
- [ ] GDPR compliance tools

#### Scalability
- [ ] Microservices architecture
- [ ] Cloud deployment optimization
- [ ] High availability setup
- [ ] Performance monitoring

#### Business Intelligence
- [ ] Real-time dashboards
- [ ] Custom report builder
- [ ] Data export/import tools
- [ ] Third-party BI tool integration

### Continuous Improvements

#### Code Quality
- [ ] Unit test coverage improvement
- [ ] Code documentation enhancement
- [ ] Performance benchmarking
- [ ] Security vulnerability assessments

#### User Training
- [ ] Interactive user tutorials
- [ ] Video training materials
- [ ] Administrator certification program
- [ ] Best practices documentation

## 🛠️ Development Guidelines

### Code Standards
- Follow Odoo development guidelines
- Implement proper error handling
- Use translation strings for all user-facing text
- Maintain backward compatibility

### Testing
- Write unit tests for all model methods
- Implement integration tests for workflows
- Test multi-language functionality
- Validate security access rules

### Documentation
- Update technical documentation with changes
- Maintain user guide accuracy
- Document API endpoints
- Keep changelog updated

## 📞 Support

### Documentation
- [Odoo Official Documentation](https://www.odoo.com/documentation)
- [Module-specific Wiki](./wiki)

### Community
- Submit issues on GitHub
- Join community discussions
- Contribute to development

### Professional Support
For professional support and customization services, contact the development team.

## 📝 License

This module is licensed under LGPL-3.0. See LICENSE file for details.

## 🤝 Contributing

We welcome contributions! Please read our [Contributing Guide](CONTRIBUTING.md) for details on how to submit pull requests, report issues, and suggest enhancements.

---

**Version**: 1.0  
**Last Updated**: December 2024  
**Compatibility**: Odoo 16.0+  
**Language Support**: Arabic, English  
**Region**: Gulf Countries (Saudi Arabia focus)
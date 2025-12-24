# Air Ticket Request Module

A comprehensive Odoo module for managing employee air ticket requests, designed specifically for organizations operating in the Gulf region with support for complex sponsorship systems and regulatory compliance.

## 📋 Overview

The Air Ticket Request module handles all aspects of employee travel requests including vacation tickets, business trip arrangements, and final exit procedures. It integrates seamlessly with Odoo's HR module and provides multi-language support (Arabic/English).

## ✨ Features

### Core Functionality
- **Multi-language Support**: Full Arabic and English interface
- **Employee Classification**: Native/Non-native nationality handling
- **Flexible Payment Options**: Employee share deduction from salary or cash payment
- **Document Management**: Iqama and passport information tracking
- **Integration**: Seamless integration with HR leaves and employee records

### Request Types
- **Leave Requests**: Annual vacation and personal leave
- **Cash Allowance**: Air ticket cash alternatives
- **Business Trips**: Deputation and business travel
- **Final Exit**: End of service travel arrangements
- **Other**: Flexible category for special cases

### Approval Workflow
- **Multi-level Approval**: Structured approval process
- **Status Tracking**: Real-time status updates
- **Mail Integration**: Automated notifications and activity tracking
- **Manager Assignment**: Automatic manager identification

### Financial Management
- **Employee Share Calculation**: Configurable employee contribution
- **Payment Methods**: Salary deduction or cash payment options
- **Cost Allocation**: Automatic allocation and tracking
- **Balance Management**: Integration with employee balance systems

## 🚀 Installation

### Prerequisites
- Odoo 16.0 or later
- Required modules: `base`, `mail`, `hr`, `hr_holidays`, `account`

### Installation Steps

1. **Copy module to addons directory**:
   ```bash
   cp -r custom_addons/air_ticket_request /path/to/odoo/addons/
   ```
   
   Or add to Odoo configuration:
   ```bash
   # In odoo.conf
   addons_path = /path/to/odoo/addons,/path/to/project/custom_addons
   ```

2. **Restart Odoo server**:
   ```bash
   sudo systemctl restart odoo
   ```

3. **Install module**:
   - Navigate to Apps menu in Odoo
   - Update the app list
   - Search for "Air Ticket Request"
   - Click Install

## ⚙️ Configuration

### Initial Setup

1. **Air Ticket Types Configuration**:
   ```
   Navigate to: HR → Configuration → Air Ticket Types
   ```
   - Define ticket categories (Economy, Business, First Class)
   - Set pricing and allocation rules
   - Configure eligibility criteria

2. **Employee Information Setup**:
   - Ensure employee records contain:
     - Iqama number and expiry date
     - Passport number and expiry date
     - Manager assignment
     - Department assignment
     - Nationality classification

3. **Sequence Configuration**:
   ```
   Navigate to: Settings → Technical → Sequences
   ```
   - Customize air ticket request numbering
   - Set up company-specific prefixes

### Access Rights

Configure user groups and permissions:
- **Employee**: Create and view own requests
- **Manager**: Approve team requests
- **HR Manager**: Full access to all requests
- **Administrator**: System configuration

## 📚 User Guide

### For Employees

#### Creating an Air Ticket Request

1. **Navigate to HR → Air Ticket Requests**
2. **Click "Create"**
3. **Complete the Request Form**:
   - **Basic Information**:
     - Description of the request
     - Employee selection (auto-filled)
     - Request reason (Leave, Business Trip, etc.)
   
   - **Travel Details**:
     - Travel date
     - Expected return date
     - Ticket type selection
     - Reservation type (Employee only or Employee + Family)
   
   - **Financial Options**:
     - Employee share amount
     - Payment method (Salary deduction or Cash)

4. **Submit for Approval**:
   - Save the request
   - Status changes to "New"
   - Automatic notification sent to manager

#### Tracking Request Status

- **New**: Request created, pending review
- **Reviewed**: Under manager evaluation
- **Approved**: Request approved and processing
- **Refused**: Request denied with explanation

### For Managers

#### Reviewing Requests

1. **Access Pending Requests**:
   ```
   HR → Air Ticket Requests → Filter: "To Review"
   ```

2. **Evaluation Process**:
   - Verify employee eligibility
   - Check leave balance integration
   - Review travel dates and purpose
   - Validate financial information

3. **Approval Actions**:
   - **Approve**: Move to approved status
   - **Request Changes**: Send back with comments
   - **Refuse**: Deny with detailed reason

### For HR Administrators

#### Request Management

1. **Monitor All Requests**:
   - Dashboard view of pending requests
   - Status distribution analysis
   - Employee request history

2. **System Administration**:
   - Configure air ticket types
   - Manage employee allocations
   - Update policy parameters

3. **Reporting**:
   - Generate request reports
   - Track approval patterns
   - Monitor budget allocations

## 🔧 Technical Details

### Module Structure
```
air_ticket_request/
├── __init__.py              # Module initialization
├── __manifest__.py          # Module manifest
├── controllers/
│   ├── __init__.py
│   └── main.py             # Web controllers
├── data/
│   └── sequence_air_ticket_request.xml  # Sequences
├── models/
│   ├── __init__.py
│   ├── air_ticket.py       # Main request model
│   ├── air_ticked_type.py  # Ticket types
│   ├── air_ticket_batch.py # Batch processing
│   ├── air_ticket_automatic_allocation.py
│   ├── air_ticket_balance_allocation.py
│   ├── country_inherit.py  # Country extensions
│   └── hr_leave.py         # Leave integration
├── security/
│   └── ir.model.access.csv # Access rights
├── static/description/     # Module assets
└── views/
    ├── air_ticket_form.xml # Main form view
    ├── air_ticked_type.xml # Type configuration
    ├── air_ticket_batch_views.xml
    ├── air_ticket_automatic_allocation.xml
    ├── air_ticket_balance_allocation.xml
    └── country_inherit.xml
```

### Key Models

#### air.ticket.request
Main model handling ticket requests with fields:
- **Basic Info**: name, description, state, employee_id
- **Employee Data**: manager_id, department_id, nationality info
- **Travel Details**: travel_date, ticket_type, reservation_type
- **Financial**: employee_share, payment_method, cash_allowed

#### air.ticket.type
Configuration model for ticket categories:
- **Type Definition**: name, code, description
- **Rules**: eligibility_criteria, allocation_rules
- **Pricing**: base_cost, employee_contribution

### Integration Points

- **HR Employee**: Employee master data
- **HR Leave**: Leave request integration
- **Mail System**: Notifications and tracking
- **Accounting**: Financial integration

## 🚀 Enhancement Roadmap

### Phase 1: Core Improvements
- [ ] Performance optimization for large datasets
- [ ] Enhanced search and filtering capabilities
- [ ] Mobile-responsive interface
- [ ] Bulk approval functionality

### Phase 2: Advanced Features
- [ ] Advanced analytics dashboard
- [ ] Automated eligibility checking
- [ ] Document attachment system
- [ ] Email template customization

### Phase 3: Integration
- [ ] External booking system integration
- [ ] Government portal connectivity
- [ ] Banking system integration
- [ ] API development for third-party systems

### Phase 4: Intelligence
- [ ] AI-powered request validation
- [ ] Predictive analytics for travel patterns
- [ ] Smart approval recommendations
- [ ] Automated document processing

## 🛠️ Development

### Extending the Module

1. **Custom Fields**:
   ```python
   # In your custom module
   class AirTicketRequest(models.Model):
       _inherit = 'air.ticket.request'
       
       custom_field = fields.Char(string='Custom Field')
   ```

2. **Custom Validation**:
   ```python
   @api.constrains('travel_date')
   def _check_travel_date(self):
       for record in self:
           if record.travel_date < fields.Date.today():
               raise ValidationError("Travel date cannot be in the past")
   ```

### API Usage

Access requests programmatically:
```python
# Search requests
requests = self.env['air.ticket.request'].search([
    ('state', '=', 'approved'),
    ('employee_id', '=', employee_id)
])

# Create request
request = self.env['air.ticket.request'].create({
    'employee_id': employee_id,
    'description': 'Annual vacation ticket',
    'request_reason': 'leave',
    'travel_date': '2024-07-15'
})
```

## 📝 Support

### Common Issues

1. **Request Not Appearing**: Check user access rights
2. **Approval Workflow Issues**: Verify manager assignment
3. **Integration Problems**: Ensure dependent modules are installed

### Documentation
- Module technical documentation in `/docs`
- API reference in code comments
- User training materials in `/training`

### Community
- Report issues on project repository
- Feature requests via GitHub issues
- Community discussions in project wiki

---

**Version**: 1.0  
**Compatibility**: Odoo 16.0+  
**Languages**: Arabic, English  
**License**: LGPL-3.0